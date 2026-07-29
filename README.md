
# 💼 Pocket C.A.

### AI-Powered Indian Income Tax Assistant using Graph RAG


# 📖 Overview

Pocket C.A. is an AI-powered tax assistant designed to simplify Indian Income Tax guidance.

Instead of searching through lengthy Income Tax Acts, Rules, Circulars, and Notifications, users can simply ask questions in natural language and receive accurate, citation-backed responses generated from official tax documents.

The system combines Graph-based Retrieval-Augmented Generation (Graph RAG), Knowledge Graphs, Large Language Models, and semantic search to provide trustworthy answers.

---

# ✨ Features

✅ AI-powered Tax Assistant

✅ Graph RAG Knowledge Base

✅ Citation-backed Responses

✅ Intelligent Tax Calculations

✅ Personalized User Tax Profile

✅ Conversation Memory

✅ Income Tax Act & Rules Search

✅ FastAPI REST API

✅ Modern Responsive Web Interface

✅ Automatic Knowledge Graph Rebuilding

---

# 🧠 How It Works

```text
                User Question
                      │
                      ▼
              FastAPI Backend
                      │
                      ▼
            Query Understanding
                      │
                      ▼
        Hybrid Graph Retrieval (RAG)
        ├──────────────┐
        │              │
        ▼              ▼
  Neo4j Graph      Semantic Search
        │              │
        └──────┬───────┘
               ▼
        Relevant Tax Chunks
               │
               ▼
        OpenAI / LLM Reasoning
               │
               ▼
 Citation-backed Final Response
```

---

# 🏗️ System Architecture

```
Frontend (HTML/CSS/JS)
          │
          ▼
      FastAPI Server
          │
          ▼
    Chatbot Orchestrator
          │
          ▼
 ┌────────────────────────────┐
 │       Graph RAG Engine      │
 └────────────────────────────┘
          │
     ┌────┴─────┐
     ▼          ▼
Neo4j KG   LlamaIndex Retriever
     │          │
     └────┬─────┘
          ▼
     OpenAI GPT Model
          │
          ▼
   Citation-based Answer
```

---

# 🚀 Key Technologies

| Category | Technologies |
|----------|--------------|
| Backend | FastAPI |
| Language | Python |
| Database | Neo4j |
| AI | OpenAI GPT |
| Framework | LangChain |
| RAG | LlamaIndex |
| Graph Database | Neo4j |
| PDF Processing | PyMuPDF |
| ORM | SQLAlchemy |

---

# 📂 Project Structure

```
PocketCA/
│
├── frontend/
│
├── data/
│
├── api_models.py
├── chatbot.py
├── chat_memory.py
├── chat_tools.py
├── graph_store.py
├── retriever.py
├── ingest.py
├── query_engine.py
├── metadata_extractor.py
├── citation_builder.py
├── rebuild_manager.py
├── profile_store.py
├── db.py
├── config.py
├── models.py
├── main.py
├── requirement.txt
│
└── README.md
```

---

# 🔥 Core Modules

### 🤖 AI Chatbot

Handles conversations using OpenAI models with tool calling capabilities.

---

### 📚 Knowledge Graph

Stores:

- Tax Documents
- Pages
- Chunks
- Sections
- Keywords
- Statutory References

inside Neo4j.

---

### 🔎 Hybrid Retriever

Retrieves information using:

- Graph Search
- Full-text Search
- Section Search
- Statutory Reference Search
- Reciprocal Rank Fusion

---

### 📑 Citation Builder

Every generated answer includes citations showing:

- Source document
- Page number
- Section title
- Statutory reference

---

### 👤 User Tax Profile

Stores personalized information including:

- Tax Regime
- Income Details
- Deductions
- Financial Year
- Assessment Year
- Previous Chat Context

---

### 💬 Conversation Memory

Maintains user sessions to provide context-aware conversations.

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/<YOUR_USERNAME>/PocketCA.git
```

```
cd PocketCA
```

---

## Install Dependencies

```bash
pip install -r requirement.txt
```

---

## Configure Environment Variables

Create a `.env` file.

```env
OPENAI_API_KEY=your_api_key

OPENAI_CHAT_MODEL=gpt-4.1-mini

NEO4J_URI=bolt://localhost:7687

NEO4J_USERNAME=neo4j

NEO4J_PASSWORD=password

NEO4J_DATABASE=neo4j
```

---

## Start the Server

```bash
uvicorn main:app --reload
```

Server:

```
http://127.0.0.1:8000
```

---

# 📷 Screenshots

### Home Page

> Add Screenshot

---

### Chat Interface

> Add Screenshot

---

### Knowledge Graph

> Add Screenshot

---

# 🎯 Example Questions

```
What is Section 80C?

Calculate tax for ₹12 lakh salary.

Difference between Old and New Tax Regime?

Can I claim HRA deduction?

What is the due date for ITR filing?

What deductions are available under Section 80D?

How much tax will I pay after deductions?
```

---

# 🚀 Future Improvements

- Voice Assistant
- OCR for Tax Documents
- PDF Upload Support
- Multi-language Support
- GST Assistant
- Income Tax Calculator UI
- AI-generated Tax Planning
- WhatsApp Integration
- Docker Deployment
- Authentication & User Accounts

---

# 🤝 Contributing

Contributions are welcome!

```bash
Fork

Create Branch

Commit Changes

Push Branch

Open Pull Request
```

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Developer

**Rakesh Kumar**

🎓 B.Tech Computer Science Engineering

💡 AI • Data Science • Cloud Computing • Graph RAG • LLM Applications

GitHub:
https://github.com/Rakesh509-ui

---

<div align="center">

### ⭐ If you like this project, consider giving it a Star!

**Made with ❤️ using Python, FastAPI, Neo4j, Graph RAG, LlamaIndex & OpenAI**

</div>
