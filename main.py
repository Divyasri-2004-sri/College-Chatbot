from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

# Load .env file for API key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Load college_info.txt content
try:
    with open("college_info.txt", "r", encoding="utf-8") as f:
        COLLEGE_INFO = f.read()
except FileNotFoundError:
    COLLEGE_INFO = "College information not available."

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
                "HTTP-Referer": "http://localhost"  # Adjust this if needed
            },
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful assistant for a college chatbot. "
                            "Use the following information about the college to help answer questions:\n\n"
                            f"{COLLEGE_INFO}"
                        )
                    },
                    {"role": "user", "content": user_input}
                ]
            }
        )

        result = response.json()

        if "choices" in result:
            answer = result["choices"][0]["message"]["content"].strip()
        else:
            error_detail = result.get("error", "No valid response from OpenRouter.")
            answer = f"Error from OpenRouter: {error_detail}"

    except Exception as e:
        answer = f"Error: {str(e)}"

    return {"data": [answer]}
