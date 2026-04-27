import os
import pandas as pd
from neo4j import GraphDatabase
from pathlib import Path

# Thông tin cấu hình Neo4j (lấy từ biến môi trường của Docker hoặc dùng mặc định)
URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "learnmart_graph_password")

def build_kb():
    # Kiểm tra đường dẫn khi chạy trong Docker hoặc chạy Local
    if Path('/app/data/data_user500.csv').exists():
        csv_path = Path('/app/data/data_user500.csv')
    else:
        # Nếu chạy trực tiếp trên Windows sẽ nối vào thư mục data
        repo_root = Path(__file__).resolve().parents[1]
        csv_path = repo_root / 'ai_chat_service' / 'data' / 'data_user500.csv'
        URI_LOCAL = "bolt://localhost:7687"
        global URI
        URI = URI_LOCAL
        
    print(f"Bắt đầu kết nối tới Neo4j tại địa chỉ: {URI}...")
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    df = pd.read_csv(csv_path)
    
    with driver.session() as session:
        print("1. Tạo các chỉ mục (Constraints) để đảm bảo không trùng lặp...")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.user_id IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Product) REQUIRE p.product_id IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (c:Category) REQUIRE c.name IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (pe:Persona) REQUIRE pe.name IS UNIQUE")
        
        print("\n2. Đang đóng gói dữ liệu và đẩy lên Knowledge Graph (Neo4j)...")
        # Đổ dữ liệu bằng phương thức siêu tốc UNWIND của Cypher thay vì chạy tuần tự
        records = df.to_dict('records')
        batch_size = 1000
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            cypher_query = """
            UNWIND $batch AS row
            
            // Khởi tạo các Thực thể (Nodes)
            MERGE (u:User {user_id: toInteger(row.user_id)})
            MERGE (p:Product {product_id: toInteger(row.product_id)})
            MERGE (c:Category {name: row.category_name})
            MERGE (pe:Persona {name: row.persona_label})
            
            // Xây dựng Mối quan hệ (Edges)
            MERGE (u)-[:BELONGS_TO]->(pe)
            MERGE (p)-[:IN_CATEGORY]->(c)
            
            // Nối hành vi tương tác 
            MERGE (u)-[r:INTERACTS_WITH {action: row.action, step: toInteger(row.step)}]->(p)
            """
            session.run(cypher_query, batch=batch)
            print(f"   -> Đã bulk-insert {i + len(batch)}/{len(records)} dòng...")
            
    driver.close()
    print("\nDONE! Xây dựng Knowledge Base Graph từ dữ liệu thành công! Bạn có thể vào http://localhost:7474 để xem.")

if __name__ == "__main__":
    build_kb()
