from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import torch
torch.backends.mkldnn.enabled = False
torch.set_num_threads(1)
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from torch import nn
from torch.nn.utils.rnn import pad_sequence, pack_padded_sequence
from torch.utils.data import DataLoader, Dataset

# =====================================================================
# 1. CẤU HÌNH & KHAI BÁO CÁC HẰNG SỐ
# =====================================================================
ACTIONS = ["search", "view", "click", "add_to_cart", "wishlist", "coupon_view", "checkout", "purchase"]
PERSONAS = ["new_explorer", "category_browser", "deal_hunter", "loyal_member", "high_intent_buyer"]
NEXT_ACTIONS = ["recommend_entry_products", "push_coupon", "bundle_related_products", "upsell_membership", "reengage_catalog"]

ACTION_TO_ID = {name: idx + 1 for idx, name in enumerate(ACTIONS)} # 0 dành cho Padding
PERSONA_TO_ID = {name: idx for idx, name in enumerate(PERSONAS)}
NBA_TO_ID = {name: idx for idx, name in enumerate(NEXT_ACTIONS)}
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# =====================================================================
# 2. XỬ LÝ DỮ LIỆU (DATASET & DATALOADER)
# =====================================================================
class BehaviorSequenceDataset(Dataset):
    def __init__(self, sequences: list[dict]): 
        self.sequences = sequences
        
    def __len__(self) -> int: 
        return len(self.sequences)
        
    def __getitem__(self, idx: int):
        row = self.sequences[idx]
        return (
            torch.tensor(row['sequence'], dtype=torch.long), 
            len(row['sequence']), 
            torch.tensor(row['persona_id'], dtype=torch.long), 
            torch.tensor(row['nba_id'], dtype=torch.long)
        )

def collate_batch(batch):
    sequences, lengths, persona_ids, nba_ids = zip(*batch)
    padded = pad_sequence(sequences, batch_first=True, padding_value=0)
    return padded, torch.tensor(lengths, dtype=torch.long), torch.stack(persona_ids), torch.stack(nba_ids)

def build_sequences(csv_path: Path) -> list[dict]:
    # Sắp xếp theo thứ tự thời gian và step để đảm bảo tính tuần tự của chuỗi
    df = pd.read_csv(csv_path).sort_values(['user_id', 'timestamp', 'step']).reset_index(drop=True)
    return [{
        'user_id': int(user_id),
        'sequence': [ACTION_TO_ID.get(action, 0) for action in group['action'].tolist()],
        'persona_id': PERSONA_TO_ID[group['persona_label'].iloc[-1]],
        'nba_id': NBA_TO_ID[group['next_best_action'].iloc[-1]],
    } for user_id, group in df.groupby('user_id')]

# =====================================================================
# 3. ĐỊNH NGHĨA KIẾN TRÚC MÔ HÌNH
# =====================================================================
class UserBehaviorRNN(nn.Module):
    def __init__(self, vocab_size: int, emb_dim: int = 64, hidden_dim: int = 64):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, emb_dim, padding_idx=0)
        self.encoder = nn.RNN(emb_dim, hidden_dim, batch_first=True, nonlinearity='tanh')
        self.dropout = nn.Dropout(0.4)
        self.persona_head = nn.Linear(hidden_dim, len(PERSONAS))
        self.nba_head = nn.Linear(hidden_dim, len(NEXT_ACTIONS))

    def forward(self, sequences, lengths):
        embedded = self.embedding(sequences)
        packed = pack_padded_sequence(embedded, lengths.cpu(), batch_first=True, enforce_sorted=False)
        _, hidden = self.encoder(packed)
        features = self.dropout(hidden[-1])
        return self.persona_head(features), self.nba_head(features)

class UserBehaviorLSTM(nn.Module):
    def __init__(self, vocab_size: int, emb_dim: int = 64, hidden_dim: int = 64):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, emb_dim, padding_idx=0)
        self.encoder = nn.LSTM(emb_dim, hidden_dim, batch_first=True)
        self.dropout = nn.Dropout(0.4)
        self.persona_head = nn.Linear(hidden_dim, len(PERSONAS))
        self.nba_head = nn.Linear(hidden_dim, len(NEXT_ACTIONS))

    def forward(self, sequences, lengths):
        embedded = self.embedding(sequences)
        packed = pack_padded_sequence(embedded, lengths.cpu(), batch_first=True, enforce_sorted=False)
        _, (hidden, _) = self.encoder(packed)
        features = self.dropout(hidden[-1])
        return self.persona_head(features), self.nba_head(features)

class UserBehaviorBiLSTM(nn.Module):
    def __init__(self, vocab_size: int, emb_dim: int = 64, hidden_dim: int = 64):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, emb_dim, padding_idx=0)
        self.encoder = nn.LSTM(emb_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.dropout = nn.Dropout(0.4)
        self.persona_head = nn.Linear(hidden_dim * 2, len(PERSONAS))
        self.nba_head = nn.Linear(hidden_dim * 2, len(NEXT_ACTIONS))

    def forward(self, sequences, lengths):
        embedded = self.embedding(sequences)
        packed = pack_padded_sequence(embedded, lengths.cpu(), batch_first=True, enforce_sorted=False)
        _, (hidden, _) = self.encoder(packed)
        features = torch.cat([hidden[-2], hidden[-1]], dim=1)
        features = self.dropout(features)
        return self.persona_head(features), self.nba_head(features)

# =====================================================================
# 4. CẤU TRÚC ĐO LƯỜNG VÀ VẼ BIỂU ĐỒ (VISUALIZATION)
# =====================================================================
@dataclass
class RunMetrics:
    model_name: str
    persona_accuracy: float
    persona_f1: float
    next_action_accuracy: float
    next_action_f1: float
    score: float # F1 trung bình (tiêu chí chọn model_best)
    epochs_run: int
    train_loss_history: list[float]
    valid_loss_history: list[float]
    train_acc_history: list[float] # Thêm mảng lưu Accuracy
    valid_acc_history: list[float] # Thêm mảng lưu Accuracy
    persona_report: dict
    next_action_report: dict

def plot_training_results(metrics: RunMetrics, output_dir: Path):
    """Vẽ biểu đồ Loss và Accuracy chung trên cùng một bức ảnh, dễ đưa vào báo cáo"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Biểu đồ 1: Loss Curve
    ax1.plot(metrics.train_loss_history, label='Train Loss', color='#1f77b4', linewidth=2)
    ax1.plot(metrics.valid_loss_history, label='Valid Loss', color='#ff7f0e', linewidth=2)
    ax1.set_title(f'[{metrics.model_name.upper()}] Loss Curve')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Biểu đồ 2: Accuracy Curve
    ax2.plot(metrics.train_acc_history, label='Train Accuracy', color='#2ca02c', linewidth=2)
    ax2.plot(metrics.valid_acc_history, label='Valid Accuracy', color='#d62728', linewidth=2)
    ax2.set_title(f'[{metrics.model_name.upper()}] Accuracy Curve')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.6)

    fig.tight_layout()
    fig.savefig(output_dir / f'{metrics.model_name}_training_curves.png', dpi=200)
    plt.close(fig)

# =====================================================================
# 5. HUẤN LUYỆN VÀ ĐÁNH GIÁ (TRAIN & EVALUATE)
# =====================================================================
def evaluate(model: nn.Module, loader: DataLoader):
    model.eval()
    loss_fn = nn.CrossEntropyLoss()
    total_loss, total_correct, total_samples = 0.0, 0, 0
    pt, pp, nt, npred = [], [], [], []
    
    with torch.no_grad():
        for sequences, lengths, persona_ids, nba_ids in loader:
            sequences, lengths = sequences.to(DEVICE), lengths.to(DEVICE)
            persona_ids, nba_ids = persona_ids.to(DEVICE), nba_ids.to(DEVICE)
            
            p_logits, n_logits = model(sequences, lengths)
            loss = loss_fn(p_logits, persona_ids) + loss_fn(n_logits, nba_ids)
            total_loss += loss.item()
            
            p_preds = torch.argmax(p_logits, dim=1)
            n_preds = torch.argmax(n_logits, dim=1)
            
            # Tính số lượng dự đoán đúng (Tạm tính trung bình 2 task để ra Acc chung)
            correct = ((p_preds == persona_ids).sum() + (n_preds == nba_ids).sum()).item()
            total_correct += correct
            total_samples += len(persona_ids) * 2
            
            pp.extend(p_preds.cpu().tolist())
            npred.extend(n_preds.cpu().tolist())
            pt.extend(persona_ids.cpu().tolist())
            nt.extend(nba_ids.cpu().tolist())
            
    avg_loss = total_loss / max(1, len(loader))
    avg_acc = (total_correct / max(1, total_samples)) * 100
    return {'loss': avg_loss, 'acc': avg_acc, 'p_true': pt, 'p_pred': pp, 'n_true': nt, 'n_pred': npred}

def train_model(model_name: str, train_data: list[dict], valid_data: list[dict], output_dir: Path) -> tuple[nn.Module, RunMetrics]:
    vocab_sz = len(ACTION_TO_ID) + 1
    if model_name == 'rnn': model = UserBehaviorRNN(vocab_size=vocab_sz).to(DEVICE)
    elif model_name == 'lstm': model = UserBehaviorLSTM(vocab_size=vocab_sz).to(DEVICE)
    else: model = UserBehaviorBiLSTM(vocab_size=vocab_sz).to(DEVICE)
    train_loader = DataLoader(BehaviorSequenceDataset(train_data), batch_size=32, shuffle=True, collate_fn=collate_batch)
    valid_loader = DataLoader(BehaviorSequenceDataset(valid_data), batch_size=32, shuffle=False, collate_fn=collate_batch)
    
    # Tinh chỉnh 1: Dùng Weight Decay (L2 Penalty) để chống Overfitting
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4) 
    
    # Tinh chỉnh 2: Scheduler giảm Learning Rate nếu Valid Loss không giảm
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=2)
    loss_fn = nn.CrossEntropyLoss()
    
    tr_loss_h, vl_loss_h, tr_acc_h, vl_acc_h = [], [], [], []
    best_state, best_valid = None, float('inf')
    
    # Tinh chỉnh 3: Early Stopping
    max_epochs = 40
    patience_counter = 0
    early_stop_patience = 6 
    
    actual_epochs = 0
    for epoch in range(max_epochs):
        actual_epochs += 1
        model.train()
        batch_losses = []
        correct_train, total_train = 0, 0
        
        for sequences, lengths, p_ids, n_ids in train_loader:
            sequences, lengths = sequences.to(DEVICE), lengths.to(DEVICE)
            p_ids, n_ids = p_ids.to(DEVICE), n_ids.to(DEVICE)
            
            optimizer.zero_grad()
            p_logits, n_logits = model(sequences, lengths)
            loss = loss_fn(p_logits, p_ids) + loss_fn(n_logits, n_ids)
            loss.backward()
            
            # Tinh chỉnh 4: Cắt gradient (Clip Grad Norm) chống bùng nổ đạo hàm ở RNN
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            
            optimizer.step()
            batch_losses.append(loss.item())
            
            # Tính Acc ngay trong Train
            correct_train += ((torch.argmax(p_logits, dim=1) == p_ids).sum() + (torch.argmax(n_logits, dim=1) == n_ids).sum()).item()
            total_train += len(p_ids) * 2

        train_loss = sum(batch_losses) / len(batch_losses)
        train_acc = (correct_train / total_train) * 100
        
        valid = evaluate(model, valid_loader)
        scheduler.step(valid['loss']) # Cập nhật Scheduler
        
        tr_loss_h.append(train_loss); vl_loss_h.append(valid['loss'])
        tr_acc_h.append(train_acc); vl_acc_h.append(valid['acc'])
        
        print(f"  -> Epoch [{actual_epochs:02d}/{max_epochs:02d}] | Train Loss: {train_loss:.4f} - Acc: {train_acc:.2f}% | Valid Loss: {valid['loss']:.4f} - Acc: {valid['acc']:.2f}%")
        
        # Lưu best model
        if valid['loss'] < best_valid:
            best_valid = valid['loss']
            best_state = {k: v.detach().cpu() for k, v in model.state_dict().items()}
            patience_counter = 0
        else:
            patience_counter += 1
            
        if patience_counter >= early_stop_patience:
            print(f"[{model_name.upper()}] Kích hoạt Early Stopping ở epoch {actual_epochs}.")
            break

    # Phục hồi trọng số tốt nhất để đánh giá chung cuộc
    model.load_state_dict(best_state)
    final_val = evaluate(model, valid_loader)
    
    p_f1 = f1_score(final_val['p_true'], final_val['p_pred'], average='weighted')
    n_f1 = f1_score(final_val['n_true'], final_val['n_pred'], average='weighted')
    score = (p_f1 + n_f1) / 2 # Lấy F1 trung bình làm tiêu chí chọn model
    
    metrics = RunMetrics(
        model_name, 
        round(accuracy_score(final_val['p_true'], final_val['p_pred']), 4),
        round(float(p_f1), 4),
        round(accuracy_score(final_val['n_true'], final_val['n_pred']), 4),
        round(float(n_f1), 4),
        round(float(score), 4),
        actual_epochs,
        [round(x, 4) for x in tr_loss_h], [round(x, 4) for x in vl_loss_h],
        [round(x, 2) for x in tr_acc_h], [round(x, 2) for x in vl_acc_h],
        classification_report(final_val['p_true'], final_val['p_pred'], target_names=PERSONAS, output_dict=True, zero_division=0),
        classification_report(final_val['n_true'], final_val['n_pred'], target_names=NEXT_ACTIONS, output_dict=True, zero_division=0)
    )
    
    plot_training_results(metrics, output_dir)
    return model, metrics

# =====================================================================
# 6. LUỒNG CHẠY CHÍNH (MAIN PROCESS)
# =====================================================================
def main():
    repo_root = Path(__file__).resolve().parents[1]
    if Path('/app/data/data_user500.csv').exists():
        csv_path = Path('/app/data/data_user500.csv')
        models_dir = Path('/app/models')
        reports_dir = Path('/app/reports')
    else:
        csv_path = repo_root / 'ai_chat_service' / 'data' / 'data_user500.csv'
        models_dir = repo_root / 'ai_chat_service' / 'models'
        reports_dir = repo_root / 'ai_chat_service' / 'reports'
    
    models_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    sequences = build_sequences(csv_path)
    train_data, valid_data = train_test_split(sequences, test_size=0.2, random_state=42, stratify=[x['persona_id'] for x in sequences])
    
    all_metrics = []
    best_model = None
    best_metrics = None
    
    print("Bắt đầu quy trình huấn luyện 3 kiến trúc mô hình...", flush=True)
    for model_name in ['rnn', 'lstm', 'bilstm']:
        print(f"Đang huấn luyện {model_name.upper()}...")
        model, metrics = train_model(model_name, train_data, valid_data, reports_dir)
        all_metrics.append(metrics)
        torch.save({'state_dict': model.state_dict(), 'model_name': model_name}, models_dir / f'{model_name}_sequence_model.pt')
        
        if best_metrics is None or metrics.score > best_metrics.score:
            best_metrics = metrics
            best_model = model
            
    # Lưu Model Tốt Nhất
    torch.save({'state_dict': best_model.state_dict(), 'model_name': best_metrics.model_name, 'actions': ACTIONS, 'personas': PERSONAS, 'next_actions': NEXT_ACTIONS}, models_dir / 'model_best.pt')
    
    # Kết xuất đánh giá (Báo cáo bằng lời)
    evaluation_text = (
        f"Đánh giá kết quả huấn luyện:\n"
        f"- Đã huấn luyện thành công 3 kiến trúc: RNN, LSTM và BiLSTM.\n"
        f"- Kết quả F1 Score trung bình: RNN ({all_metrics[0].score}), LSTM ({all_metrics[1].score}), BiLSTM ({all_metrics[2].score}).\n"
        f"-> CHỌN MÔ HÌNH {best_metrics.model_name.upper()} làm `model_best` vì đạt độ đo tổng hợp F1 trung bình cao nhất ({best_metrics.score:.4f}). "
        f"Mô hình này cân bằng tốt nhất giữa khả năng lưu trữ ngữ cảnh chuỗi dài (Sequence Memory) và khả năng tổng quát hóa dữ liệu trên tập Valid."
    )
    
    summary = {
        'results': [asdict(m) for m in all_metrics], 
        'best_model': best_metrics.model_name, 
        'text_evaluation': evaluation_text
    }
    
    (reports_dir / 'sequence_model_report.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    
    # Vẽ biểu đồ so sánh cuối cùng
    ranking = sorted(all_metrics, key=lambda x: x.score, reverse=True)
    fig = plt.figure(figsize=(8, 4.8))
    plt.bar([m.model_name.upper() for m in ranking], [m.score for m in ranking], color=['#2ca02c', '#1f77b4', '#ff7f0e'])
    plt.ylim(0, 1.0)
    plt.ylabel('Weighted F1 Average')
    plt.title('So sánh hiệu suất tổng hợp: RNN vs LSTM vs BiLSTM')
    for idx, val in enumerate([m.score for m in ranking]): 
        plt.text(idx, val + 0.02, f'{val:.3f}', ha='center', fontweight='bold')
    fig.tight_layout()
    fig.savefig(reports_dir / 'final_model_comparison.png', dpi=180)
    plt.close(fig)
    
    print("\n" + "="*50)
    print(evaluation_text)
    print("Đã lưu các biểu đồ Loss/Accuracy và model_best vào thư mục reports/ và models/.")

if __name__ == '__main__':
    main()