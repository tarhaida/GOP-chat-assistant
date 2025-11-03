# GOP Chat Assistant - RAG-Based Health & Safety Compliance Assistant

**A sophisticated Retrieval-Augmented Generation (RAG) system for GOP Co-Living Ltd**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)](https://python.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)](https://streamlit.io/)

---

## 🎯 Project Overview

**GOP Chat Assistant** is an intelligent document question-answering system built for GOP Co-Living Ltd, a property management company. The assistant provides instant, accurate answers to queries about health & safety policies, compliance requirements, and operational procedures by leveraging advanced Retrieval-Augmented Generation (RAG) technology.

### Key Features

- **🔍 Semantic Search**: Uses vector embeddings to find relevant information across multiple policy documents
- **💬 Interactive Chat**: Streamlit-based UI with conversation memory
- **📚 Multi-Document Support**: Handles Health & Safety Policy, Business Continuity Plans, Fire Risk Assessments, and more
- **🎯 Context-Aware Responses**: Retrieves relevant document sections and generates grounded answers
- **🔒 Secure**: API keys stored in .env, no hardcoded credentials
- **⚡ Fast**: ChromaDB vector database for instant document retrieval

---

## 🏗️ Architecture

```
User Query → Streamlit UI → Vector DB Semantic Search → Document Retrieval → LLM Response Generation → User
                                    ↓
                            ChromaDB (Persistent Storage)
                                    ↓
                        Embedded Policy Documents (HuggingFace Embeddings)
```

### Technology Stack

- **LLM**: Groq (llama3-70b-8192) via LangChain
- **Vector Database**: ChromaDB with persistent storage
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2` model
- **UI Framework**: Streamlit
- **Orchestration**: LangChain
- **Configuration**: YAML-based modular prompts

---

## 📁 Project Structure

```
Projet_COP/
├── code/
│   ├── config/
│   │   ├── config.yaml              # App configuration (LLM, vector DB settings)
│   │   └── prompt_config.yaml       # Modular system prompts
│   ├── COP_Assistant.py            # Main Streamlit application
│   ├── COP_vector_db_ingest.py     # Document ingestion script
│   ├── COP_vector_db_rag.py        # RAG retrieval logic
│   ├── paths.py                    # Path configurations
│   ├── prompt_builder.py           # Modular prompt construction
│   └── utils.py                    # Utility functions
├── data/
│   └── HEALTH AND SAFETY POLICY.md # Source documents
├── outputs/
│   └── vector_db/                  # ChromaDB persistent storage
├── .env                           # API keys (not committed)
├── .env_example                   # Template for environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.11 or higher
- Groq API key (free at [console.groq.com](https://console.groq.com/))

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/GOP-chat-assistant.git
cd GOP-chat-assistant
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

*Get your free Groq API key at [console.groq.com](https://console.groq.com/)*

### Step 5: Ingest Documents into Vector Database

```bash
python code/COP_vector_db_ingest.py
```

This will:
- Load documents from `data/` directory
- Chunk them into semantic segments
- Generate embeddings using HuggingFace transformers
- Store in ChromaDB (`outputs/vector_db/`)

### Step 6: Run the Application

```bash
streamlit run code/COP_Assistant.py
```

The assistant will open in your browser at `http://localhost:8501`

---

## 💡 How It Works

### 1. Document Ingestion

```python
# COP_vector_db_ingest.py
- Reads mGOPdown documents from data/
- Splits into chunks (512 characters with 50 char overlap)
- Generates embeddings using HuggingFace model
- Stores in ChromaDB with persistent storage
```

### 2. Query Processing

```python
# When user asks a question:
1. User query → Embedded using same HuggingFace model
2. Vector similarity search in ChromaDB (top_k=5 results)
3. Retrieved documents passed to LLM as context
4. LLM generates grounded response
5. Response displayed in Streamlit chat
```

### 3. RAG Pipeline

```python
# COP_vector_db_rag.py
def respond_to_query(query, chat_history):
    # 1. Retrieve relevant documents
    docs = vector_db.similarity_search(query, k=5)
    
    # 2. Build context-aware prompt
    prompt = build_prompt(query, docs, chat_history)
    
    # 3. Generate response
    response = llm.invoke(prompt)
    
    return response
```

---

## 📊 Use Cases

### Example Queries

**Health & Safety Compliance:**
- "What is GOP's fire safety policy?"
- "What are the emergency procedures?"
- "Who is responsible for health and safety training?"

**Operational Procedures:**
- "What are the gym equipment safety guidelines?"
- "How should contractors be selected?"
- "What is the first aid procedure?"

**Policy Details:**
- "What is covered under COSHH regulations?"
- "What are the display screen equipment requirements?"
- "What is the drugs and alcohol policy?"

---

## 🛠️ Configuration

### Modular Prompt System

Prompts are defined in `code/config/prompt_config.yaml`:

```yaml
rag_assistant_prompt:
  role: |
    You are an GOP Co-Living Health & Safety Assistant.
  
  instruction: |
    Answer questions using ONLY the provided document context.
    
  constraints:
    - If information is not in the retrieved documents, say "I don't have that information"
    - Always cite document sections when answering
    - Be concise and professional
```

### Vector Database Settings

Configured in `code/config/config.yaml`:

```yaml
vectordb:
  collection_name: "GOP_policies"
  embedding_model: "sentence-transformers/all-MiniLM-L6-v2"
  top_k: 5
  similarity_threshold: 0.7
```

---

## 🔒 Security Best Practices

✅ **API keys stored in .env file** (excluded from Git via .gitignore)  
✅ **.env_example provided** for easy setup  
✅ **No hardcoded credentials** in codebase  
✅ **Input validation** on user queries  
✅ **Rate limiting** considerations for production deployment  

---

## 📈 Future Enhancements

- [ ] Add document upload functionality
- [ ] Implement user authentication
- [ ] Add conversation export feature
- [ ] Multi-language support
- [ ] Advanced filtering (by document type, date, etc.)
- [ ] Analytics dashboard for query patterns
- [ ] Integration with GOP's internal systems

---

## 🧪 Testing

Run the ingestion script to verify setup:

```bash
python code/COP_vector_db_ingest.py
```

Expected output:
```
✅ Loaded 1 documents
✅ Created 156 chunks
✅ Generated embeddings
✅ Stored in ChromaDB collection: GOP_policies
```

---

## 📝 License

This project is part of the **Ready Tensor Agentic AI Developer Certification Program**.

Built for educational purposes as Project 1 (Module 1): RAG-Based AI Assistant.

---

## 👤 Author

**Tarik Haida, CFA**
- 📍 Geneva, Switzerland
- 📧 tarik.haida@gmail.com
- 🔗 [LinkedIn](https://linkedin.com/in/thaida)
- 🎓 [Ready Tensor Certification]([https://app.readytensor.ai/publications/gop-chat-assistant-rag-based-health-safety-compliance-system-FQSoIivtIVfv])

---

## 🙏 Acknowledgments

- Built using **Ready Tensor's Agentic AI Certification Program** Module 1 concepts
- Developed for **GOP Co-Living Ltd**
- Powered by **LangChain**, **ChromaDB**, and **Groq**

---

## 📚 Learn More

- [Ready Tensor Agentic AI Certification](https://app.readytensor.ai/certifications/agentic-ai-cert-U7HxeL7a)
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**⭐ Star this repository if you find it useful!**
