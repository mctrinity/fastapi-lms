# 🔍 Troubleshooting FAISS Scoring, Document Store Issues, and Improvements

## 🚨 **Common FAISS Issues and Fixes**

### **1️⃣ Issue: Low Scores for Relevant Documents**
#### ❌ Problem:
- FAISS retrieves documents with **low similarity scores**, even if they are relevant.
- Example: `"Ferdinand Magellan"` scores **0.4555**, below the threshold, leading to *"I don't have enough information"* response.

#### ✅ Fix:
- **Use Cosine Similarity Instead of L2 Distance**
- FAISS **IndexFlatL2** measures **Euclidean distance** (lower is better), but **IndexFlatIP** (Inner Product) is better for text (**higher is better**).

```python
faiss_index = faiss.IndexFlatIP(384)  # ✅ Switch to Inner Product for cosine similarity
```

- **Ensure Normalized Embeddings** (Cosine Similarity requires normalized vectors):

```python
embeddings = embed_model.encode(documents, normalize_embeddings=True)
faiss_index.add(np.array(embeddings, dtype=np.float32))

query_embedding = embed_model.encode([query], normalize_embeddings=True)
```

✅ **Now, FAISS scoring will be between `-1` (opposite) and `1` (perfect match).**

---

### **2️⃣ Issue: FAISS Retrieves Unrelated Documents**
#### ❌ Problem:
- FAISS pulls **random or weakly related documents** instead of the most relevant ones.
- Example: A query about **"Los Angeles"** also retrieves results about **"Beverly Hills" and "Statue of Liberty."**

#### ✅ Fix:
- **Limit FAISS to Retrieve Only the Best Match (`top_k=1`)**

```python
async def retrieve_and_generate(query: str, top_k: int = 1):  # ✅ Get only 1 most relevant doc
    query_embedding = embed_model.encode([query], normalize_embeddings=True)
    distances, indices = faiss_index.search(np.array(query_embedding, dtype=np.float32), top_k)
    
    best_match_idx = indices[0][0]  # Take only the highest-ranked document
    retrieved_doc = documents[best_match_idx]

    print(f"🔍 Best Match: {retrieved_doc} | Score: {distances[0][0]:.4f}")
```
✅ **Now, FAISS will always return the most relevant document instead of random weak matches.**

---

### **3️⃣ Issue: FAISS Discards Good Results (Similarity Threshold Too High)**
#### ❌ Problem:
- If a document's similarity score is **0.55** and the threshold is `0.6`, it gets discarded.
- Results in **"I don't have enough information"** when the document is actually relevant.

#### ✅ Fix:
- **Lower the similarity threshold** to allow more relevant documents:

```python
async def retrieve_and_generate(query: str, top_k: int = 3, similarity_threshold: float = 0.4):
```
✅ **Now, FAISS keeps slightly lower-scoring but relevant documents.**

---

### **4️⃣ Issue: Document Store is Too Small (Limited Knowledge)**
#### ❌ Problem:
- FAISS can only return documents **stored in the system**.
- If the **LMS document store lacks general knowledge**, AI fails for off-topic questions.

#### ✅ Fix:
- **Expand the Document Store** with additional knowledge:
  - Add **more general facts** to prevent knowledge gaps.
  - Store **documents in a database (SQLite, PostgreSQL, MongoDB)** instead of hardcoded lists.
  
```python
# Example expanded document store
from document_store import documents  # Load from an external source
```
✅ **Now, FAISS has more data to search from, reducing irrelevant results.**

---

### **5️⃣ Issue: FAISS Fails to Retrieve Anything (Silent Failure)**
#### ❌ Problem:
- FAISS sometimes **fails to retrieve any documents**, returning an empty response.

#### ✅ Fix:
- **Ensure FAISS Index is Properly Built** after loading documents:

```python
faiss_index = faiss.IndexFlatIP(384)  # ✅ Reinitialize FAISS
embeddings = embed_model.encode(documents, normalize_embeddings=True)  # ✅ Re-encode documents
faiss_index.add(np.array(embeddings, dtype=np.float32))  # ✅ Rebuild FAISS index
```
✅ **Now, FAISS won’t fail due to missing index data.**

---

### **6️⃣ Issue: Tokenizer Parallelism Causing Deadlocks**
#### ❌ Problem:
- FAISS and Hugging Face **tokenizers** sometimes create deadlocks due to multiprocessing.
- You may see warnings like:
  > "huggingface/tokenizers: The current process just got forked, after parallelism has already been used."

#### ✅ Fix:
- **Disable parallelism before running FAISS:**

```python
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # ✅ Prevents multiprocessing deadlocks
```
✅ **Now, FAISS and Hugging Face models work without multiprocessing conflicts.**

---

## 🎯 **Final Optimizations for FAISS Retrieval**
| **Issue** | **Fix Applied** |
|------------|---------------|
| **Low scores for relevant docs** | Switched FAISS to **IndexFlatIP** (cosine similarity) |
| **Randomly retrieved documents** | Limited FAISS to **top_k=1** (only best match) |
| **Good documents discarded** | Lowered **similarity threshold to 0.4** |
| **Document store too small** | Expanded **document knowledge base** |
| **FAISS index issues** | Rebuilt FAISS index with **normalized embeddings** |
| **Tokenizer deadlocks** | Disabled **TOKENIZERS_PARALLELISM** to prevent multiprocessing errors |

---

## 🔑 **Key Takeaways**
- **FAISS scoring depends on correct distance metric** (Use `IndexFlatIP` for cosine similarity).
- **Normalization is crucial** for accurate similarity results.
- **Setting `top_k=1` ensures the most relevant document is retrieved.**
- **Lowering the similarity threshold (`0.4`) prevents discarding useful documents.**
- **Expanding the document store increases knowledge coverage.**
- **Disabling `TOKENIZERS_PARALLELISM` prevents multiprocessing deadlocks.**

🚀 **Now, your FAISS retrieval system is stable, accurate, and only returns relevant results!** 🔥🔥🔥
