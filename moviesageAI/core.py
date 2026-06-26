# MovieSage AI bot
# 1 take a raw para about a movie
# 2 Extract important structured info
# 3 Generate a clean summary
# 4 Returns it into JSON Format

import sys
from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
from pydantic import BaseModel
from typing import List, Optional

# Initialize ChatGroq model directly
model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)

class Movie(BaseModel):
    title: str
    genre: Optional[str] = None
    director: Optional[str] = None
    writers: Optional[str] = None
    producers: Optional[str] = None
    cast: Optional[List[str]] = None
    release_year: Optional[int] = None
    runtime: Optional[str] = None
    language: Optional[str] = None
    country: Optional[List[str]] = None
    plot_summary: Optional[str] = None
    main_characters: Optional[List[str]] = None
    themes: Optional[List[str]] = None
    notable_facts: Optional[List[str]] = None
    awards: Optional[List[str]] = None
    box_office: Optional[str] = None
    rating: Optional[str] = None
    keywords: Optional[List[str]] = None

parser = PydanticOutputParser(pydantic_object=Movie)

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
8. Return ONLY valid JSON conforming to the requested schema.
9. Do not include markdown, explanations, comments, or additional text.

{format_instructions}
""",
        ),
        (
            "human",
            """
Analyze the following movie description and extract all relevant information.

Movie Description:
{movie_description}
""",
        ),
    ]
)

print("Paste your movie description below.")
print("When done, press Ctrl+Z then Enter (Windows) or Ctrl+D (Mac/Linux):")
print("-" * 50)
para = sys.stdin.read().strip()

if not para:
    print("No input provided. Exiting.")
    sys.exit(0)

final_prompt = prompt.invoke(
    {
        "movie_description": para,
        "format_instructions": parser.get_format_instructions()
    }
)

print("\nExtracting information... Please wait...")
res = model.invoke(final_prompt)

# Parse output using Pydantic parser
try:
    parsed_movie = parser.parse(res.content)
    print("\nStructured Movie Intelligence (JSON):")
    print(parsed_movie.model_dump_json(indent=2))
except Exception as e:
    print("\nFailed to parse model output directly into the Movie schema.")
    print("Raw output:")
    print(res.content)
    print("Error detail:", e)

# AI -> JSON -> Backend -> API -> Frontend