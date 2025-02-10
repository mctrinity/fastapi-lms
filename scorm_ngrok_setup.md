# 📌 SCORM Cloud & ngrok Integration with FastAPI

## **1️⃣ Overview**
This documentation covers how to integrate **SCORM Cloud** with a **FastAPI backend** using **ngrok** for local testing. It includes:
- Setting up SCORM Cloud for **learner tracking**
- Using **ngrok** to expose the local FastAPI server
- Handling **SCORM webhooks** and **testing API requests**
- Using **RSA keys for SCORM JWT authentication**
- Required **Python dependencies**

---

## **2️⃣ Prerequisites**
### ✅ **Install Dependencies**
```bash
pip install fastapi uvicorn requests python-dotenv pyjwt cryptography faiss-cpu numpy sentence-transformers httpx pandas scipy tqdm
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

## **3️⃣ Required Python Dependencies**
Below are the necessary dependencies for SCORM Cloud integration with FastAPI:

### ✅ **`requirements.txt`**
```plaintext
# Core FastAPI Dependencies
fastapi
uvicorn

# OpenAI API and AI Model Dependencies
openai
whisper
sentence-transformers  # ✅ Required for embeddings
torch  # ✅ Needed for PyTorch-based models (used by sentence-transformers)

# FAISS and Numerical Computing
faiss-cpu
numpy
pandas
scipy  # ✅ Useful for numerical computations & similarity search

# FastAPI Data Validation & Environment Variables
pydantic
python-dotenv

# Utility Libraries
tqdm
requests
httpx  # ✅ Required by FastAPI for async HTTP requests

# SCORM Cloud Authentication
pyjwt  # ✅ Required for JWT authentication with SCORM Cloud
cryptography  # ✅ Required for RSA-based JWT authentication (RS256)
```

---

## **4️⃣ Setting Up SCORM Cloud**
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

## **5️⃣ Setting Up ngrok for Local Testing**
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

🚀 **Now SCORM Cloud is successfully integrated with FastAPI and ngrok using RSA authentication!** 🚀

