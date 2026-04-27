# AGENT MASTER GUIDE - PROJECT REFACTOR & AI SERVICE

> [!IMPORTANT]
> **DEADLINE:** Monday, April 27th @ 11:30 PM.
> **Current Status:** Reorganized into Microservices structure with a Hybrid Architecture (Django + FastAPI). Core services are in `backend-services/`.

## 1. Project Context
- **Course:** Software Architecture (SoAD).
- **Goal:** Build a complete E-commerce system with Microservices & AI.
- **Tech Stack:** 
    - **Backend:** **Django + DRF** (Core services like Auth, Product, Order) & **FastAPI** (AI services, API Gateway).
    - **Database:** MySQL (Structured), Neo4j (Graph for AI), RabbitMQ (Messaging).
    - **Frontend:** React Native / Web (folder `frontend`).
    - **Deployment:** Docker Compose (Ports prefix 80xx).

## 2. Directory Structure (Refactored)
- `/backend-services/`: All 14 microservices (auth, product, ai_chat, etc).
- `/docs/agent-docs/`: AI context, refactor notes, and architecture diagrams.
- `/docs/raw-docs/`: Original assignment PDFs and older reference configs.
- `/scripts/`: Migration, seeding, and fix scripts.
- `/api_gateway`, `/frontend`, `/nginx`: Main entry points at root.

## 3. Tonight's AI Service Deliverables (Checklist)
Based on `baitap_NOP_ai_service_20.04.2026_new.pdf`:
- [ ] **Data Generation:** Generate `data_user500.csv` with 500 users and 8 behavior types (view, click, add_to_cart).
- [ ] **AI Models:** Train RNN/LSTM/biLSTM models for next-action prediction. Choose `model_best`.
- [ ] **Knowledge Graph:** Sync user behavior data into **Neo4j**.
- [ ] **RAG System:** Build a RAG-based chatbot using the Knowledge Graph.
- [ ] **Integration:** 
    - Display recommendations when searching/adding to cart.
    - Custom Chat UI (not ChatGPT style).

## 4. Key Configurations
- **Docker Compose:** Uses `.env` for variables. 
- **Volumes:** Reuses `shopx_mysql_data` and `shopx_neo4j_data` (External).
- **Auth:** JWT-based, shared across services. Secret key in `.env`.

## 5. Instructions for AI Agents
- Always maintain the `backend-services/` structure.
- When fixing code, look for **DDD patterns** in `product_service` (using `JSONField` for attributes) and replicate them if refactoring others.
- Priority for April 27th: **Verify Django Migration & AI Integration**.
