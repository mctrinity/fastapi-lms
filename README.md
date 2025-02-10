# 📌 Project README: FastAPI LMS with Next.js Frontend

## 🚀 **Project Overview**
This project is a **Learning Management System (LMS)** that integrates **FastAPI (Backend)** and **Next.js (Frontend)** with **FAISS-based Retrieval-Augmented Generation (RAG)** using OpenAI's GPT model.

### **Tech Stack**
- **Backend:** FastAPI, FAISS, OpenAI API, SentenceTransformers
- **Frontend:** Next.js, React, TailwindCSS
- **Database:** FAISS-based Document Store (for Retrieval)

---

## 🔧 **Backend Setup (FastAPI)**

### **1️⃣ Clone Repository & Setup Virtual Environment**
```sh
git clone https://github.com/your-repo-name.git
cd backend
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

### **2️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **3️⃣ Configure Environment Variables**
Create a `.env` file and add:
```sh
OPENAI_API_KEY=your_openai_api_key_here
```

### **4️⃣ Run FastAPI Backend**
```sh
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### **5️⃣ Test API Endpoints**
- Open **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- Open **Redoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🎨 **Frontend Setup (Next.js + TailwindCSS)**

### **1️⃣ Create Next.js Frontend**
```sh
npx create-next-app@latest frontend
```

### **2️⃣ Move to Frontend Directory & Install Dependencies**
```sh
cd frontend
npm install
```

### **2️⃣ Run Next.js Development Server**
```sh
npm run dev
```
- Open [http://localhost:3000](http://localhost:3000) in your browser.

### **3️⃣ Build for Production**
```sh
npm run build
```

### **4️⃣ Run Production Server**
```sh
npm start
```

---

## 📂 **Project Structure**
```
├── backend
│   ├── app.py  # FastAPI main application
│   ├── document_store.py  # FAISS document retrieval (Control Group for AI)
│   ├── requirements.txt  # Backend dependencies
│   ├── .env  # Environment variables
│   └── ...
│
├── frontend
│   ├── app
│   │   ├── page.tsx  # Home Page Component
│   │   ├── layout.tsx  # Global Layout
│   │   ├── globals.css  # Tailwind Global Styles
│   ├── next.config.js  # Next.js Configurations
│   ├── tailwind.config.ts  # Tailwind Configurations
│   ├── package.json  # Frontend Dependencies
│   ├── .eslintrc.js  # ESLint Configurations
│   └── ...
```

📝 **Note:** `document_store.py` serves as the **control group** for the AI. It defines the dataset that the AI can retrieve from, ensuring responses remain relevant to the LMS context.

---

## ⚠️ **Troubleshooting & Fixes**

### **1️⃣ `.ts` vs `.js` vs `.mjs` - Which One to Use?**
| Extension | Purpose |
|-----------|---------|
| `.js` | Standard JavaScript files |
| `.ts` | TypeScript files (adds type safety) |
| `.mjs` | Modern JavaScript module format |

✅ **Use `.ts` for TypeScript projects** and `.mjs` if your project uses **ECMAScript Modules (ESM)**.

---

### **2️⃣ TailwindCSS Not Working (`Unknown at rule @tailwind`)**
#### ✅ Fix:
Ensure Tailwind is installed and correctly configured.
```sh
npm install -D tailwindcss postcss autoprefixer
```
Update `postcss.config.js`:
```js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

---

### **3️⃣ FastAPI Fails to Retrieve Documents (`I don't have enough information`)**
#### ✅ Fix:
1. Ensure FAISS uses **cosine similarity**:
   ```python
   faiss_index = faiss.IndexFlatIP(384)
   ```
2. Normalize embeddings before adding them:
   ```python
   embeddings = embed_model.encode(documents, normalize_embeddings=True)
   faiss_index.add(np.array(embeddings, dtype=np.float32))
   ```
3. Reduce `similarity_threshold` if results are being discarded.
   ```python
   similarity_threshold = 0.4
   ```

---

### **4️⃣ Next.js Not Compiling (`Error: Unexpected any`)**
#### ✅ Fix:
Edit `eslint.config.mjs` to allow `any` if necessary:
```js
const eslintConfig = {
  rules: {
    '@typescript-eslint/no-explicit-any': 'off',
  },
};
export default eslintConfig;
```

---

## 🎯 **Key Takeaways**
✅ Use **FastAPI** for backend efficiency.  
✅ Use **Next.js** for a modern frontend framework.  
✅ FAISS improves document retrieval for **RAG-based AI**.  
✅ `.ts` for **TypeScript**, `.mjs` for **ES Modules**, `.js` for **legacy JS**.  
✅ **Normalize embeddings** for better FAISS performance.  
✅ Set **`top_k=1`** for precise retrieval.  
✅ Use **lower similarity thresholds (`0.4`)** to prevent discarding useful results.  
✅ **Document Store (`document_store.py`) ensures AI stays within context, preventing unrelated responses.**  

🚀 **Your LMS AI system is now fully functional!** 🎉🔥
