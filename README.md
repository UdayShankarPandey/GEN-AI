# 🤖 GENAIPEP — GenAI with LangChain & Groq

A hands-on collection of LangChain-powered chatbot and AI projects using **Groq's ultra-fast LLM inference** and **HuggingFace embeddings**.

## 📁 Project Structure

```
GENAIPEP/
├── chatmodel/
│   ├── Chat.py              # Single-turn chat demo
│   ├── Chatbot.py           # Multi-turn terminal chatbot with personalities
│   ├── UIchatbot.py         # 🎭 MoodBot — Streamlit personality chatbot
│   └── Huggingface.py       # HuggingFace Inference endpoint demo
├── moviesageAI/
│   ├── core.py              # 🎬 MovieSage CLI — extract JSON from movie descriptions
│   └── UIMoviesagebot.py    # 🎬 MovieSage Streamlit UI
├── embedding.py             # 🔢 Text embeddings with bge-large-en-v1.5
├── test.py                  # Quick import/version check
├── requirements.txt         # All dependencies
├── .env.example             # API key template
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

---

## 🎭 MoodBot — Personality Chatbot

Pick a personality and chat with an AI that fully stays in character.

**Run:**
```bash
streamlit run chatmodel/UIchatbot.py
# Opens at http://localhost:8501
```

| Personality | Vibe |
|-------------|------|
| 😂 Funny | Jokes and puns for every answer |
| 😤 Angry | EVERYTHING IS UNACCEPTABLE |
| 🙄 Sarcastic | Oh wow, what a great question |
| 😢 Sad | Everything hurts, but ok |
| 💕 Romantic | Every word is a love letter |

---

## 🎬 MovieSage AI — Movie Information Extractor

Paste any movie description and get back fully structured JSON with title, cast, director, plot summary, themes, awards, box office, and more.

**Run Streamlit UI:**
```bash
streamlit run moviesageAI/UIMoviesagebot.py
# Opens at http://localhost:8502
```

**Run CLI:**
```bash
python moviesageAI/core.py
# Paste description → press Ctrl+Z + Enter (Windows) to submit
```

**Example output:**
```json
{
  "title": "The Dark Knight",
  "genre": "superhero",
  "director": "Christopher Nolan",
  "cast": ["Heath Ledger"],
  "release_year": 2008,
  "box_office": "$1 billion",
  "awards": ["2 Oscars"],
  "keywords": ["superhero", "Joker", "Batman"]
}
```

---

## 🔢 Embeddings — `embedding.py`

Generates high-quality semantic embeddings using `BAAI/bge-large-en-v1.5` (~1.34 GB, 1024-dim).

```bash
python embedding.py
```

```python
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en-v1.5",
    model_kwargs={"device": "cpu", "trust_remote_code": True},
    encode_kwargs={"normalize_embeddings": True},  # Required for BGE models
)
vector = embeddings.embed_query("What is LangChain?")
# → 1024-dimensional float vector
```

### Embedding Model Comparison

| Model | Size | Dim | Use Case |
|-------|------|-----|----------|
| `BAAI/bge-large-en-v1.5` ✅ | ~1.34 GB | 1024 | Best quality English |
| `BAAI/bge-base-en-v1.5` | ~440 MB | 768 | Balanced |
| `BAAI/bge-small-en-v1.5` | ~67 MB | 384 | Lightweight/dev |

---

## 💬 Terminal Chatbot — `chatmodel/Chatbot.py`

Multi-turn terminal chatbot with selectable personalities and conversation memory.

```bash
python chatmodel/Chatbot.py
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **LangChain** | LLM orchestration framework |
| **Groq** | Ultra-fast LLM inference (`llama-3.3-70b-versatile`) |
| **HuggingFace** | Local embedding models |
| **Streamlit** | Web UI for MoodBot & MovieSage |
| **python-dotenv** | Environment variable management |
| **FAISS** | Vector similarity search (ready to use) |

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

Never commit your `.env` file — it's already in `.gitignore`.
Use `.env.example` as a safe template to share required keys.
