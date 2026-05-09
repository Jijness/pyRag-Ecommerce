import numpy as np

def _relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(0.0, x)

def _relu_grad(x: np.ndarray) -> np.ndarray:
    return (x > 0).astype(np.float64)

def _softmax(x: np.ndarray) -> np.ndarray:
    shifted = x - np.max(x, axis=1, keepdims=True)
    exp_scores = np.exp(shifted)
    return exp_scores / np.sum(exp_scores, axis=1, keepdims=True)

def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -35, 35)))

class DeepClassifierV2:
    """Numpy-based Deep Neural Network with Adam Optimizer, L2 Regularization, and Dropout"""
    def __init__(
        self,
        input_dim: int,
        output_dim: int,
        hidden_dims: tuple[int, ...] = (128, 64, 32),
        learning_rate: float = 0.001,
        epochs: int = 300,
        batch_size: int = 64,
        l2_lambda: float = 0.0001,
        dropout_rate: float = 0.2,
        seed: int = 42,
    ):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.hidden_dims = hidden_dims
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size
        self.l2_lambda = l2_lambda
        self.dropout_rate = dropout_rate
        self.seed = seed

        self.mean_: np.ndarray | None = None
        self.std_: np.ndarray | None = None
        
        self.weights: list[np.ndarray] = []
        self.biases: list[np.ndarray] = []
        
        # For Adam optimizer
        self.m_w: list[np.ndarray] = []
        self.v_w: list[np.ndarray] = []
        self.m_b: list[np.ndarray] = []
        self.v_b: list[np.ndarray] = []

        self.history = {'loss': [], 'accuracy': []}

    def _init_params(self):
        rng = np.random.default_rng(self.seed)
        dims = [self.input_dim, *self.hidden_dims, self.output_dim]
        self.weights = []
        self.biases = []
        self.m_w = []
        self.v_w = []
        self.m_b = []
        self.v_b = []

        for in_dim, out_dim in zip(dims[:-1], dims[1:]):
            scale = np.sqrt(2.0 / max(1, in_dim)) # He initialization
            self.weights.append(rng.normal(0.0, scale, size=(in_dim, out_dim)))
            self.biases.append(np.zeros((1, out_dim), dtype=np.float64))
            
            self.m_w.append(np.zeros((in_dim, out_dim)))
            self.v_w.append(np.zeros((in_dim, out_dim)))
            self.m_b.append(np.zeros((1, out_dim)))
            self.v_b.append(np.zeros((1, out_dim)))

    def _standardize_fit(self, x: np.ndarray) -> np.ndarray:
        self.mean_ = x.mean(axis=0, keepdims=True)
        self.std_ = x.std(axis=0, keepdims=True) + 1e-8
        return (x - self.mean_) / self.std_

    def _standardize(self, x: np.ndarray) -> np.ndarray:
        return (x - self.mean_) / self.std_

    def _forward(self, x: np.ndarray, training: bool = False):
        activations = [x]
        pre_activations = []
        dropouts = []
        current = x
        rng = np.random.default_rng(self.seed)

        for idx, (weights, bias) in enumerate(zip(self.weights, self.biases)):
            z = current @ weights + bias
            pre_activations.append(z)
            
            if idx == len(self.weights) - 1:
                current = _softmax(z) # Output layer
            else:
                current = _relu(z) # Hidden layer
                # Dropout
                if training and self.dropout_rate > 0:
                    mask = rng.binomial(1, 1 - self.dropout_rate, size=current.shape) / (1 - self.dropout_rate)
                    current = current * mask
                    dropouts.append(mask)
                else:
                    dropouts.append(None)
                    
            activations.append(current)
            
        return activations, pre_activations, dropouts

    def fit(self, x_train: np.ndarray, y_train: np.ndarray):
        x_norm = self._standardize_fit(x_train.astype(np.float64))
        self._init_params()
        sample_count = len(x_norm)
        
        # Adam params
        beta1, beta2, epsilon = 0.9, 0.999, 1e-8
        t = 0

        for epoch in range(self.epochs):
            rng = np.random.default_rng(self.seed + epoch)
            indices = rng.permutation(sample_count)
            epoch_loss = 0
            epoch_correct = 0

            for start in range(0, sample_count, self.batch_size):
                batch_idx = indices[start : start + self.batch_size]
                batch_x = x_norm[batch_idx]
                batch_y = y_train[batch_idx]
                m_size = len(batch_x)

                activations, pre_activations, dropouts = self._forward(batch_x, training=True)
                probs = activations[-1]
                
                # Cross entropy loss with L2
                batch_loss = -np.sum(batch_y * np.log(probs + 1e-15)) / m_size
                l2_loss = sum(np.sum(w**2) for w in self.weights) * (self.l2_lambda / (2 * m_size))
                epoch_loss += (batch_loss + l2_loss) * m_size
                
                # Accuracy
                epoch_correct += np.sum(np.argmax(probs, axis=1) == np.argmax(batch_y, axis=1))

                # Backprop
                grad = (probs - batch_y) / m_size
                t += 1

                for layer in reversed(range(len(self.weights))):
                    a_prev = activations[layer]
                    
                    grad_w = a_prev.T @ grad + (self.l2_lambda / m_size) * self.weights[layer]
                    grad_b = np.sum(grad, axis=0, keepdims=True)

                    # Adam update
                    self.m_w[layer] = beta1 * self.m_w[layer] + (1 - beta1) * grad_w
                    self.v_w[layer] = beta2 * self.v_w[layer] + (1 - beta2) * (grad_w ** 2)
                    m_w_hat = self.m_w[layer] / (1 - beta1 ** t)
                    v_w_hat = self.v_w[layer] / (1 - beta2 ** t)
                    
                    self.m_b[layer] = beta1 * self.m_b[layer] + (1 - beta1) * grad_b
                    self.v_b[layer] = beta2 * self.v_b[layer] + (1 - beta2) * (grad_b ** 2)
                    m_b_hat = self.m_b[layer] / (1 - beta1 ** t)
                    v_b_hat = self.v_b[layer] / (1 - beta2 ** t)

                    self.weights[layer] -= self.learning_rate * m_w_hat / (np.sqrt(v_w_hat) + epsilon)
                    self.biases[layer] -= self.learning_rate * m_b_hat / (np.sqrt(v_b_hat) + epsilon)

                    if layer > 0:
                        grad = grad @ self.weights[layer].T
                        if dropouts[layer-1] is not None:
                            grad = grad * dropouts[layer-1]
                        grad = grad * _relu_grad(pre_activations[layer - 1])
            
            self.history['loss'].append(epoch_loss / sample_count)
            self.history['accuracy'].append(epoch_correct / sample_count)

    def predict_proba(self, x_pred: np.ndarray) -> np.ndarray:
        x_norm = self._standardize(x_pred.astype(np.float64))
        activations, _, _ = self._forward(x_norm, training=False)
        return activations[-1]

    def predict(self, x_pred: np.ndarray, labels: list[str]) -> list[str]:
        probs = self.predict_proba(x_pred)
        indices = np.argmax(probs, axis=1)
        return [labels[int(idx)] for idx in indices]


class DeepRegressorV2(DeepClassifierV2):
    """Regressor variation"""
    def _forward(self, x: np.ndarray, training: bool = False):
        activations = [x]
        pre_activations = []
        dropouts = []
        current = x
        rng = np.random.default_rng(self.seed)

        for idx, (weights, bias) in enumerate(zip(self.weights, self.biases)):
            z = current @ weights + bias
            pre_activations.append(z)
            
            if idx == len(self.weights) - 1:
                current = _sigmoid(z) # Sigmoid for 0-1 continuous output
            else:
                current = _relu(z)
                if training and self.dropout_rate > 0:
                    mask = rng.binomial(1, 1 - self.dropout_rate, size=current.shape) / (1 - self.dropout_rate)
                    current = current * mask
                    dropouts.append(mask)
                else:
                    dropouts.append(None)
                    
            activations.append(current)
        return activations, pre_activations, dropouts

    def fit(self, x_train: np.ndarray, y_train: np.ndarray):
        x_norm = self._standardize_fit(x_train.astype(np.float64))
        self._init_params()
        sample_count = len(x_norm)
        y_target = y_train.reshape(-1, 1).astype(np.float64)
        
        beta1, beta2, epsilon = 0.9, 0.999, 1e-8
        t = 0

        for epoch in range(self.epochs):
            rng = np.random.default_rng(self.seed + epoch)
            indices = rng.permutation(sample_count)
            epoch_loss = 0

            for start in range(0, sample_count, self.batch_size):
                batch_idx = indices[start : start + self.batch_size]
                batch_x = x_norm[batch_idx]
                batch_y = y_target[batch_idx]
                m_size = len(batch_x)

                activations, pre_activations, dropouts = self._forward(batch_x, training=True)
                preds = activations[-1]
                
                # MSE Loss
                batch_loss = np.sum((preds - batch_y)**2) / (2 * m_size)
                l2_loss = sum(np.sum(w**2) for w in self.weights) * (self.l2_lambda / (2 * m_size))
                epoch_loss += (batch_loss + l2_loss) * m_size

                # Backprop (MSE + Sigmoid grad)
                grad = (preds - batch_y) * preds * (1.0 - preds) / m_size
                t += 1

                for layer in reversed(range(len(self.weights))):
                    a_prev = activations[layer]
                    grad_w = a_prev.T @ grad + (self.l2_lambda / m_size) * self.weights[layer]
                    grad_b = np.sum(grad, axis=0, keepdims=True)

                    self.m_w[layer] = beta1 * self.m_w[layer] + (1 - beta1) * grad_w
                    self.v_w[layer] = beta2 * self.v_w[layer] + (1 - beta2) * (grad_w ** 2)
                    m_w_hat = self.m_w[layer] / (1 - beta1 ** t)
                    v_w_hat = self.v_w[layer] / (1 - beta2 ** t)
                    
                    self.m_b[layer] = beta1 * self.m_b[layer] + (1 - beta1) * grad_b
                    self.v_b[layer] = beta2 * self.v_b[layer] + (1 - beta2) * (grad_b ** 2)
                    m_b_hat = self.m_b[layer] / (1 - beta1 ** t)
                    v_b_hat = self.v_b[layer] / (1 - beta2 ** t)

                    self.weights[layer] -= self.learning_rate * m_w_hat / (np.sqrt(v_w_hat) + epsilon)
                    self.biases[layer] -= self.learning_rate * m_b_hat / (np.sqrt(v_b_hat) + epsilon)

                    if layer > 0:
                        grad = grad @ self.weights[layer].T
                        if dropouts[layer-1] is not None:
                            grad = grad * dropouts[layer-1]
                        grad = grad * _relu_grad(pre_activations[layer - 1])
            
            self.history['loss'].append(epoch_loss / sample_count)

    def predict(self, x_pred: np.ndarray) -> np.ndarray:
        x_norm = self._standardize(x_pred.astype(np.float64))
        activations, _, _ = self._forward(x_norm, training=False)
        return activations[-1].reshape(-1)
