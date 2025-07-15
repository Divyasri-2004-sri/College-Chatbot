from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

# Load .env file for API key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# FastAPI app setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class Question(BaseModel):
    data: list[str]

@app.get("/")
async def root():
    return {"message": "College chatbot API (OpenRouter) is running."}

@app.post("/api/predict")
async def predict(question: Question):
    user_input = question.data[0]

    try:
        # API request to OpenRouter
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost"  # Required by OpenRouter
            },
            json={
                "model": "mistralai/mistral-7b-instruct",  # or another available model
                "messages": [
                    {"role": "system", "content": "You are a helpful college assistant."},
                    {"role": "user", "content": user_input}
                ]
            }
        )

        result = response.json()
        answer = result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        answer = f"Error: {str(e)}"

    return {"data": [answer]}
