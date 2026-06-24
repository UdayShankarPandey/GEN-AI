from dotenv import load_dotenv

load_dotenv()
from langchain_mistralai import ChatMistralAI

# two issues are here 1st Short term memory 2nd Large context window and no roles are defined
messages = []
print("______________welcome type 0 to exit this app_______________ ")
while True:
    prompt = input("YOU: ")
    messages.append(prompt)
    if prompt == "0":
        break
    model = ChatMistralAI(model="mistral-small-2603")
    res = model.invoke(messages)
    messages.append(res.content)
    print("BOT:", res.content)
    print(messages)
