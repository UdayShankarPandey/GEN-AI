# 🤖 GENAIPEP — GenAI with LangChain & Groq

A hands-on collection of LangChain-powered chatbot and embedding scripts using **Groq's ultra-fast LLM inference** and **HuggingFace embeddings**.

## 📁 Project Structure

```
GENAIPEP/
├── chatmodel/
│   ├── Chat.py          # Single-turn chat demo
│   ├── Chatbot.py       # Multi-turn terminal chatbot with personalities
│   ├── UIchatbot.py     # 🌟 Full Streamlit UI chatbot (MoodBot)
│   └── Huggingface.py   # HuggingFace Inference endpoint demo
├── embedding.py         # 🔢 Text embeddings with bge-large-en-v1.5
├── test.py              # Quick import/version check
├── requirements.txt     # All dependencies
├── .env.example         # API key template
└── .gitignore
```

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/UdayShankarPandey/GEN-AI.git
cd GEN-AI
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```
Get a free Groq API key at: https://console.groq.com

### 4. Run the app

**🌟 Streamlit UI (recommended):**
```bash
streamlit run chatmodel/UIchatbot.py
```

**Terminal chatbot:**
```bash
python chatmodel/Chatbot.py
```

**Single-turn demo:**
```bash
python chatmodel/Chat.py
```

**Text embeddings:**
```bash
python embedding.py
```

---

## 🎭 MoodBot — Streamlit UI

MoodBot lets you pick a personality and chat with an AI that stays in character:

| Personality | Vibe |
|-------------|------|
| 😂 Funny | Jokes and puns for every answer |
| 😤 Angry | EVERYTHING IS UNACCEPTABLE |
| 🙄 Sarcastic | Oh wow, what a great question |
| 😢 Sad | Everything hurts, but ok |
| 💕 Romantic | Every word is a love letter |

---

## 🔢 Embeddings — `embedding.py`

Generates high-quality semantic embeddings using `BAAI/bge-large-en-v1.5` (~1.34 GB, 1024-dim).

```python
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en-v1.5",
    model_kwargs={"device": "cpu", "trust_remote_code": True},
    encode_kwargs={"normalize_embeddings": True},  # Required for BGE models
)

vector = embeddings.embed_query("What is LangChain?")
# → 1024-dimensional float vector
```

### Why `normalize_embeddings=True`?
BGE models are trained with **cosine similarity** — normalization ensures correct similarity scores when used with FAISS or any vector store.

### Embedding Model Comparison

| Model | Size | Dim | Use Case |
|-------|------|-----|----------|
| `BAAI/bge-large-en-v1.5` ✅ | ~1.34 GB | 1024 | Best quality English |
| `BAAI/bge-base-en-v1.5` | ~440 MB | 768 | Balanced |
| `BAAI/bge-small-en-v1.5` | ~67 MB | 384 | Lightweight/dev |

---

## 🛠️ Tech Stack

- **LangChain** — LLM orchestration framework
- **Groq** — Ultra-fast LLM inference (`llama-3.3-70b-versatile`)
- **HuggingFace** — Local embedding models
- **Streamlit** — Web UI
- **python-dotenv** — Environment variable management

## 📦 Key Dependencies

| Package | Purpose |
|---------|---------|
| `langchain-groq` | Groq LLM integration |
| `langchain-core` | Core LangChain primitives |
| `langchain-huggingface` | HuggingFace embeddings |
| `streamlit` | Web UI framework |
| `faiss-cpu` | Vector similarity search |
| `python-dotenv` | `.env` file loader |

## 🔐 Security

Never commit your `.env` file. The `.gitignore` is already configured to exclude it.
Use `.env.example` as a safe template to share required keys.
