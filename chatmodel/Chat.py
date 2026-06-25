# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()
from langchain_groq import ChatGroq


# model = ChatOpenAI(model_name="gpt-5.4-mini-2026-03-17")
# res = model.invoke("Hii Chatgpt how are you")
# print(res.content)


# model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
# res = model.invoke("Hii gemini how are you")
# print(res.content)


# model = ChatGroq(model="openai/gpt-oss-120b")
# res = model.invoke("Tell me about GENAI")
# print(res.content)

# model = init_chat_model("groq:openai/gpt-oss-120b")
# res = model.invoke("Tell me about LPU")
# print(res.content)
model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.9, max_tokens=100)
res = model.invoke("write a poem for me on the beauty of nature")
print(res.content)
