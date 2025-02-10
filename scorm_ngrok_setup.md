# 📌 SCORM Cloud & ngrok Integration with FastAPI

## **1️⃣ Overview**
This documentation covers how to integrate **SCORM Cloud** with a **FastAPI backend** using **ngrok** for local testing. It includes:
- Setting up SCORM Cloud for **learner tracking**
- Using **ngrok** to expose the local FastAPI server
- Handling **SCORM webhooks** and **testing API requests**
- Using **RSA keys for SCORM JWT authentication**

---

## **2️⃣ Prerequisites**
### ✅ **Install Dependencies**
```bash
pip install fastapi uvicorn requests python-dotenv pyjwt cryptography faiss-cpu numpy sentence-transformers
```

### ✅ **Create Required Files**
Ensure you have the following files in your **FastAPI project**:
```
backend/
  ├── app.py  # FastAPI backend
  ├── .env    # Environment variables
  ├── scorm_private_key.pem  # Private RSA Key for SCORM Cloud
  ├── scorm_public_key.pem   # Public RSA Key for SCORM Cloud
```

### ✅ **Generate RSA Keys for SCORM Authentication**
SCORM Cloud requires **JWT authentication using RSA keys**. Follow these steps to generate your key pair:
```bash
openssl genpkey -algorithm RSA -out backend/scorm_private_key.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -in backend/scorm_private_key.pem -pubout -out backend/scorm_public_key.pem
```
- `scorm_private_key.pem` → Used to **sign JWT tokens**
- `scorm_public_key.pem` → Uploaded to **SCORM Cloud** for verification

### ✅ **ngrok Account Required**
You need a **ngrok account** to use ngrok for exposing your local server.
1. **Sign up for a free account**: [ngrok Signup](https://dashboard.ngrok.com/signup)
2. **Get your authtoken** from: [ngrok Authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
3. **Authenticate ngrok** (see Step 4 below)

---

## **3️⃣ Setting Up SCORM Cloud**
### **1️⃣ Create a SCORM Cloud App**
1. Log in to **SCORM Cloud** → Go to **Apps**
2. Click **Create a New App**
3. Copy **SCORM_APP_ID** and **SCORM_SECRET_KEY**
4. Upload **scorm_public_key.pem** under **Security Settings**

### **2️⃣ Configure SCORM Cloud Webhook**
1. Navigate to **Apps > Your App > Application Settings**
2. Set **Import Post Back URL** to:
   ```
   https://your-ngrok-url.ngrok.io/api/results
   ```
   *(Replace `your-ngrok-url.ngrok.io` with your actual ngrok URL.)*

3. Save changes.

---

## **4️⃣ Setting Up ngrok for Local Testing**
### ✅ **Install ngrok**
```bash
brew install ngrok  # macOS
sudo apt install ngrok  # Linux
choco install ngrok  # Windows
```

### ✅ **Authenticate ngrok**
```bash
ngrok config add-authtoken YOUR_AUTHTOKEN
```

### ✅ **Start ngrok**
```bash
ngrok http 8000
```
- Copy the **public URL** from ngrok output.
- Use this URL in **SCORM Cloud Import Post Back URL**.

---

## **5️⃣ FastAPI Code Updates (`app.py`)**

### **✅ Configure FastAPI & CORS**
```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cloud.scorm.com"],
    allow_methods=["*"]
)
```

### **✅ Generate SCORM JWT Token Using RSA**
```python
import jwt, time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

SCORM_PRIVATE_KEY_PATH = "backend/scorm_private_key.pem"
SCORM_APP_ID = "your-app-id"

def generate_scorm_token():
    with open(SCORM_PRIVATE_KEY_PATH, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )
    
    payload = {
        "iss": SCORM_APP_ID,
        "sub": SCORM_APP_ID,
        "aud": "SCORM",
        "exp": int(time.time()) + 3600
    }
    return jwt.encode(payload, private_key, algorithm="RS256")
```

### **✅ SCORM Webhook Listener (Handles SCORM Cloud Webhooks)**
```python
@app.api_route("/api/results", methods=["GET", "POST"])
async def receive_scorm_results(request: Request):
    if request.method == "GET":
        params = dict(request.query_params)
        print("🔍 Received SCORM Data via GET:", params)
        return {"status": "success", "method": "GET", "data": params}

    data = await request.json()
    print("🔍 Received SCORM Data via POST:", data)
    return {"status": "success", "method": "POST", "data": data}
```

---

🚀 **Now SCORM Cloud is successfully integrated with FastAPI and ngrok using RSA authentication!** 🚀

