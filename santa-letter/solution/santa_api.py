from fastapi import FastAPI
from pydantic import BaseModel
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-10-21"
)

class Letter(BaseModel):
    name: str
    age: int
    behavior: str
    letter_content: str

@app.post("/send_letter")
def send_letter(letter: Letter):
    system_prompt = "You are Santa Claus, a friendly, kind and cool figure who responds warmly to children's letters."
    user_prompt = f"Dear Santa Claus,\n\nMy name is {letter.name}, I am {letter.age} years old, and I have been {letter.behavior} this year. Here is my letter:\n\n{letter.letter_content}\n\nBest wishes,\n{letter.name}"
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=500
    )
    
    print(response.choices[0].message.content.strip())

    return {"santa_response": response.choices[0].message.content.strip()}