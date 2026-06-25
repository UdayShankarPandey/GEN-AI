# 🤖 GENAIPEP — GenAI with LangChain & Groq

A hands-on collection of LangChain-powered chatbot scripts using **Groq's ultra-fast LLM inference** (llama-3.3-70b-versatile).

## 📁 Project Structure

```
GENAIPEP/
├── chatmodel/
│   ├── Chat.py          # Single-turn chat demo
│   ├── Chatbot.py       # Multi-turn terminal chatbot with personalities
│   ├── UIchatbot.py     # 🌟 Full Streamlit UI chatbot (MoodBot)
│   └── Huggingface.py   # HuggingFace Inference endpoint demo
├── test.py              # Quick import/version check
├── requirements.txt     # All dependencies
├── .env.example         # API key template
└── .gitignore
```

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/SuyashGupta007/GENAIPEP.git
cd GENAIPEP
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

## 🎭 MoodBot — Streamlit UI

MoodBot lets you pick a personality and chat with an AI that stays in character:

| Personality | Vibe |
|-------------|------|
| 😂 Funny | Jokes and puns for every answer |
| 😤 Angry | EVERYTHING IS UNACCEPTABLE |
| 🙄 Sarcastic | Oh wow, what a great question |
| 😢 Sad | Everything hurts, but ok |
| 💕 Romantic | Every word is a love letter |

## 🛠️ Tech Stack

- **LangChain** — LLM orchestration framework
- **Groq** — Ultra-fast LLM inference (llama-3.3-70b-versatile)
- **Streamlit** — Web UI
- **python-dotenv** — Environment variable management

## 📦 Key Dependencies

| Package | Purpose |
|---------|---------|
| `langchain-groq` | Groq LLM integration |
| `langchain-core` | Core LangChain primitives |
| `streamlit` | Web UI framework |
| `python-dotenv` | `.env` file loader |

## 🔐 Security

Never commit your `.env` file. The `.gitignore` is already configured to exclude it.
Use `.env.example` as a safe template to share required keys.
