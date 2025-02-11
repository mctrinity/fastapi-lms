from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from document_store import documents  # ✅ Import external document store
import jwt  # ✅ Install using: pip install pyjwt
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Load environment variables from .env
load_dotenv()

# Retrieve API Keys from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SCORM_APP_ID = os.getenv("SCORM_APP_ID")
SCORM_PRIVATE_KEY_PATH = os.getenv("SCORM_PRIVATE_KEY_PATH")

# Ensure API keys are available
if not OPENAI_API_KEY:
    raise ValueError("🚨 OPENAI_API_KEY is missing! Check your .env file.")

if not SCORM_APP_ID or not SCORM_PRIVATE_KEY_PATH:
    raise ValueError(
        "🚨 SCORM_APP_ID or SCORM_PRIVATE_KEY_PATH is missing! Check your .env file."
    )

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

# ✅ Enable CORS for frontend requests + SCORM Cloud
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://cloud.scorm.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Define API request model
class QueryRequest(BaseModel):
    query: str


# ✅ Load SentenceTransformer Model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
faiss_index = faiss.IndexFlatL2(384)  # 384-dimensional embeddings

# ✅ Encode and store documents in FAISS index
embeddings = embed_model.encode(documents)
faiss_index.add(np.array(embeddings, dtype=np.float32))


# ✅ Generate SCORM Cloud Authentication Token using RS256
def generate_scorm_token():
    """Generate a valid JWT token for SCORM Cloud API authentication using RS256"""
    if not SCORM_PRIVATE_KEY_PATH or not os.path.exists(SCORM_PRIVATE_KEY_PATH):
        raise FileNotFoundError(
            f"🚨 RSA private key not found at {SCORM_PRIVATE_KEY_PATH}"
        )

    with open(SCORM_PRIVATE_KEY_PATH, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )

    payload = {
        "iss": SCORM_APP_ID,
        "sub": SCORM_APP_ID,
        "aud": "SCORM",
        "exp": int(time.time()) + 3600,  # Token expires in 1 hour
    }

    token = jwt.encode(payload, private_key, algorithm="RS256")

    # Debugging Output
    print(f"\n🔍 Generated JWT Payload: {payload}")
    print(f"🔑 Generated JWT Token: {token}\n")

    return token


# ✅ Function to Perform Retrieval-Augmented Generation (RAG)
async def retrieve_and_generate(query: str, top_k: int = 1):
    query_embedding = embed_model.encode([query], normalize_embeddings=True)
    distances, indices = faiss_index.search(
        np.array(query_embedding, dtype=np.float32), top_k
    )
    best_match_idx = indices[0][0]
    retrieved_doc = documents[best_match_idx]

    prompt = f"""You are an AI assistant. Answer the question based on the following information:
    
    Question: {query}
    Retrieved Information: {retrieved_doc}
    
    Provide a detailed response.
    Answer:
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.7,
    )

    return {
        "retrieved_doc": retrieved_doc,
        "response": response.choices[0].message.content.strip(),
    }


# ✅ API Route for Query Processing
@app.post("/query")
async def handle_query(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    result = await retrieve_and_generate(request.query)
    return result


@app.get("/")
async def home():
    return {"message": "FastAPI LMS is running!"}
