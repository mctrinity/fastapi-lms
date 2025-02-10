from fastapi import FastAPI, HTTPException  # ✅ Import HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Retrieve API Key from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure API key is available
if not OPENAI_API_KEY:
    raise ValueError("🚨 OPENAI_API_KEY is missing! Check your .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()


# Define request model
class QueryRequest(BaseModel):
    query: str


@app.post("/query")
async def handle_query(request: QueryRequest):
    # ✅ Check if query is empty
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": request.query}],
        max_tokens=500,
    )
    return {"response": response.choices[0].message.content}


@app.get("/")
async def home():
    return {"message": "FastAPI LMS is running!"}
