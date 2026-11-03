import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
print("MODEL in .env:", os.getenv("MODEL"))

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

for m in client.models.list():
    print(m.id)