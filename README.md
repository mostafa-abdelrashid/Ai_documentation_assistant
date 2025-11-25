# 📘 AI Documentation Assistant  
An end-to-end system that analyzes source code using LLMs, generates architectural insights, and produces full Markdown documentation (available as a pdf also) with a Streamlit frontend UI and FastAPI backend.

---

## 🚀 Overview  
The **AI Documentation Assistant** is a dual-model system designed to:

- Analyze code: purpose, components, dependencies, configuration  
- Extract architecture details: design patterns, data flow, and relationships  
- Generate full Markdown documentation automatically  
- Provide a user-friendly frontend for interacting with the backend  

It uses **CodeLlama** for code analysis & architecture reasoning, and **Mistral-Nemo-Instruct-2407** for documentation generation.

---

## 🏗️ Project Structure
📦 ai-documentation-assistant  
├── kaggle_backend.ipynb  # FastAPI backend with LLM pipeline    
├── app.py # Streamlit UI  
├── .env # API key + backend URL  

---

## 🧠 Features

### **Backend (FastAPI + LangChain + HF models)**
- Runs two LLMs:
  - 🔹 *CodeLlama 7B Instruct* — code reasoning  
  - 🔹 *Mistral-Nemo-Instruct-2407* — documentation generation  
- Uses chains for:
  - Code analysis  
  - Architecture extraction  
  - Markdown documentation generation  
- Fully automated pipeline using structured output schemas  
- Exposes `/generate` endpoint  
- Authentication via Bearer API key  
- Ngrok tunneling for public usage  

### **Frontend (Streamlit UI)**
- Paste code or a prompt to generate documentation  
- Three tabs:
  - 📝 Analysis  
  - 🏗️ Architecture  
  - 📄 Documentation (Preview + Raw Markdown + PDF Download)  
- Converts Markdown → HTML → PDF using WeasyPrint  
- Clean UX with expanders and layout sections  

---

## 🔧 Installation & Setup

### **1. Clone the Repo**

```bash
git clone https://github.com/your-username/ai-documentation-assistant.git
cd ai-documentation-assistant
⚙️ Backend Setup (FastAPI)
```

### **2. Install Backend Dependencies**

```bash
pip install -r backend/requirements.txt
Dependencies include:
fastapi, uvicorn, langchain, transformers, torch, bitsandbytes, pyngrok
```
### **3. Environment Variables**
Create a file:

backend/.env

```ini
API_KEY=your_api_key_here
NGROK_TOKEN=your_ngrok_token_here
```
### **4. Run Backend**  
```bash
python backend/main.py
```
You will see:

```cpp
Your public URL: https://xxxx.ngrok.io
```
Use this URL in the frontend.

## 🖥️ Frontend Setup (Streamlit)
### **1. Install Frontend Requirements**
```bash
pip install -r frontend/requirements.txt
```
### **2. Create .env inside frontend**
```
ini
API_KEY=your_api_key_here
BACKEND_URL=https://xxxx.ngrok.io/generate
```

### **3. Run Streamlit App**
```bash
streamlit run frontend/app.py
```
## 🧪 Usage Workflow

### **1. Paste Your Code**
Paste any code snippet into the text box.

### **2. Click “Generate Documentation”**

The backend pipeline will:

Analyze your code

Detect architecture

Generate full documentation

### **3. Explore Results in Tabs**
📝 Analysis

🏗️ Architecture

📄 Documentation (preview + raw markdown + PDF export)

📡 API Usage (Manual)
Send POST request to backend:
```
bash
curl -X POST "{BACKEND_URL}" \
 -H "Authorization: Bearer YOUR_API_KEY" \
 -H "Content-Type: application/json" \
 -d '{"prompt": "your code here"}'
```
Response format:
```
json
{
  "response": [
    { "analysis": {...}},
    { "architecture": {...}},
    { "doc": {...}}
  ]
}
```
📄 Example Output
The system produces:

Code purpose

Key components

Architecture diagram description

Full Markdown documentation

## 🧱 Technologies Used
- HuggingFace Models(CodeLlama 7B Instruct, Mistral-Nemo-Instruct-2407)
- LangChain
- Ngrok
- FastAPI
- Quantization : BitsAndBytes (4-bit quantization)
- Streamlit
- WeasyPrint
- Output parsers
- llm chains

