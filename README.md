# College Chatbot (FastAPI + OpenAI)

A simple college assistant chatbot using FastAPI and OpenAI's Chat API.

## Setup

1. Create `.env` file with:
    ```
    OPENAI_API_KEY=your_key_here
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Run the app:
    ```
    uvicorn main:app --reload
    ```

## Deploy

Deploy to Render or other services and set your API key as an environment variable.

# College Chatbot API

This is a FastAPI-powered chatbot backend using OpenRouter.ai. It uses college_info.txt to answer user queries.

## Setup

1. Copy `.env.example` to `.env` and add your OpenRouter API key:
   ```bash
   cp .env.example .env
