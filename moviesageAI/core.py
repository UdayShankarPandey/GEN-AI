# MovieSage AI bot
# 1. Take a raw paragraph about a movie
# 2. Extract important structured info
# 3. Generate a clean summary
# 4. Return it in JSON format

from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
import json

model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are MovieSage AI, an expert movie analyst and information extraction assistant.

Your responsibilities:
1. Carefully read and understand the entire movie description.
2. Extract all important movie-related information.
3. Generate a concise and engaging plot summary.
4. Identify key characters, themes, and notable facts.
5. Extract factual information only from the provided text.
6. If information is not available, return null.
7. Never hallucinate or invent details.
8. Return ONLY valid JSON — no markdown, no extra text.

Extract the following fields:
- title, genre, director, writers, producers, cast, release_year, runtime
- language, country, plot_summary, main_characters, themes
- notable_facts, awards, box_office, rating, keywords
""",
        ),
        (
            "human",
            "Analyze the following movie description and extract all relevant information.\n\nMovie Description:\n{movie_description}",
        ),
    ]
)

chain = prompt | model | StrOutputParser()

# ── Test run ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sample = """
    Inception (2010) is a science fiction action film written and directed by Christopher Nolan.
    The film stars Leonardo DiCaprio as a professional thief who steals information by entering
    the subconscious mind of his targets. He is offered a chance to have his criminal history erased
    as payment for the implantation of another person's idea into a target's subconscious.
    The supporting cast includes Joseph Gordon-Levitt, Elliot Page, Tom Hardy, Ken Watanabe, and Cillian Murphy.
    The film was a massive box office success, grossing over $836 million worldwide.
    It won four Academy Awards including Best Cinematography.
    """

    result = chain.invoke({"movie_description": sample})
    print(result)

    try:
        parsed = json.loads(result)
        print("\n✅ Valid JSON parsed successfully")
        print(f"Title: {parsed.get('title')}")
        print(f"Director: {parsed.get('director')}")
        print(f"Plot: {parsed.get('plot_summary')}")
    except json.JSONDecodeError:
        print("\n⚠️ Response is not valid JSON — model returned plain text")
        print(result)
