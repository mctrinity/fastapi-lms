# 📌 SCORM Cloud & ngrok Integration with FastAPI

## **1️⃣ Overview**
This documentation covers how to integrate **SCORM Cloud** with a **FastAPI backend** using **ngrok** for local testing. It includes:
- Setting up SCORM Cloud for **learner tracking**
- Using **ngrok** to expose the local FastAPI server
- Handling **SCORM webhooks** and **testing API requests**
- Using **RSA keys for SCORM JWT authentication**
- Required **Python dependencies**
- **Comparison of SCORM Cloud, Azure, AWS, and TalentLMS**
- **Uploading SCORM Content & Supported File Types**

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

## **3️⃣ Uploading SCORM Content & Supported File Types**
### **🔹 Supported SCORM File Types**
SCORM Cloud and SCORM-compliant LMS platforms accept **SCORM packages** in `.zip` format. The `.zip` file must contain:
- **SCORM Manifest File (`imsmanifest.xml`)** → Defines course structure
- **HTML, CSS, JavaScript** → For interactive learning content
- **Multimedia Files** (Videos, Images, Audio, PDFs)

### **🔹 SCORM Versions Supported**
| SCORM Format | Description |
|--------------|------------|
| **SCORM 1.2** | Most widely used, simpler but limited tracking |
| **SCORM 2004 (2nd, 3rd, 4th Edition)** | Advanced tracking, sequencing, and reporting |

### **🔹 Uploading SCORM Packages to SCORM Cloud**
#### ✅ **Manual Upload**
1. **Log in to SCORM Cloud** → **Courses > Add Course**
2. **Click “Upload SCORM Package”**
3. **Select a `.zip` SCORM file** and upload
4. **Launch & Test the Course**

#### ✅ **Upload via API**
SCORM Cloud provides an API for automatic course uploads:
```python
import requests

SCORM_CLOUD_API = "https://cloud.scorm.com/api/v2"
SCORM_API_KEY = "your-api-key"

def upload_scorm_course(file_path):
    headers = {"Authorization": f"Bearer {SCORM_API_KEY}"}
    files = {"file": open(file_path, "rb")}
    
    response = requests.post(f"{SCORM_CLOUD_API}/courses/importJobs", headers=headers, files=files)
    
    return response.json()

# Example usage:
print(upload_scorm_course("course.zip"))
```

### **🔹 Authoring Tools to Create SCORM Courses**
If you don’t have SCORM content, you can **create courses** using these tools:
| Tool | SCORM Support | Best For |
|------|--------------|----------|
| **Articulate Storyline** | ✅ SCORM 1.2 & 2004 | Interactive courses |
| **Adobe Captivate** | ✅ SCORM 1.2 & 2004 | Software simulations |
| **iSpring Suite** | ✅ SCORM 1.2 & 2004 | PowerPoint-based content |
| **H5P** | ❌ (Requires LMS integration) | HTML5-based interactive content |

---

## **4️⃣ Comparing Azure, AWS, SCORM Cloud, and TalentLMS**
Each of these platforms serves different purposes in **e-learning and SCORM content delivery**.

### **🔹 Overview of Each Platform**
| Platform    | Purpose | SCORM Support | LMS Features | Custom Development |
|------------|---------|--------------|--------------|--------------------|
| **Microsoft Azure** | Cloud computing & AI services | ❌ No built-in SCORM | ❌ No native LMS | ✅ Can build a custom LMS with Azure services |
| **Amazon Web Services (AWS)** | Cloud computing | ❌ No built-in SCORM | ❌ No native LMS | ✅ Can build a custom LMS using AWS tools |
| **SCORM Cloud** | SCORM Hosting & Tracking | ✅ Fully SCORM-compliant | ❌ Not a full LMS | ✅ API access for custom SCORM integrations |
| **TalentLMS** | Learning Management System (LMS) | ✅ Fully SCORM-compliant | ✅ Built-in LMS features | ❌ Limited customization |

### **🔹 Which One Should You Choose?**
| Use Case | Best Option |
|----------|------------|
| **I need a full LMS with SCORM & tracking** | ✅ **TalentLMS** |
| **I only need SCORM hosting & tracking** | ✅ **SCORM Cloud** |
| **I want to build a custom LMS using cloud services** | ✅ **Azure or AWS** |
| **I need an API-driven SCORM hosting service** | ✅ **SCORM Cloud** |

🚀 **Now SCORM Cloud is successfully integrated with FastAPI and ngrok using RSA authentication!** 🚀

Would you like help **storing SCORM data in a database?** 😊
