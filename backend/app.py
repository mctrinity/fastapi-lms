from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
from document_store import documents  # ✅ Import external document store

# Load environment variables from .env
load_dotenv()

# Retrieve API Key from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["TOKENIZERS_PARALLELISM"] = (
    "false"  # ✅ Prevents deadlocks in Hugging Face tokenizers
)

# Ensure API key is available
if not OPENAI_API_KEY:
    raise ValueError("🚨 OPENAI_API_KEY is missing! Check your .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

# ✅ Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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


# ✅ Function to Perform Retrieval-Augmented Generation (RAG)
async def retrieve_and_generate(
    query: str, top_k: int = 1
):  # 🔥 Get only 1 most relevant doc
    query_embedding = embed_model.encode([query], normalize_embeddings=True)

    distances, indices = faiss_index.search(
        np.array(query_embedding, dtype=np.float32), top_k
    )

    # Since we use cosine similarity, FAISS now returns similarity scores directly
    best_match_idx = indices[0][0]  # Take only the highest-ranked document
    best_match_score = distances[0][0]  # Get the highest similarity score

    # Retrieve the best matching document
    retrieved_doc = documents[best_match_idx]

    # Debugging Output
    print("\n🔍 FAISS DEBUGGING RESULTS:")
    print(f"📌 Score: {best_match_score:.4f} | Document: {retrieved_doc}")

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
