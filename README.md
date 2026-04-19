# 🤖 AI-First CRM HCP Interaction System

## 📌 Overview

This project is an **AI-powered Customer Relationship Management (CRM) system** designed for logging interactions with **Healthcare Professionals (HCPs)**.

Instead of manually filling forms, users interact with an **AI assistant**, which automatically extracts information from natural language and populates the form.

---

## 🎯 Objective

To build an **AI-first interaction logging system** where:

* Users describe interactions in natural language
* AI extracts structured data
* Form is auto-filled without manual input

---

## 🧠 Key Concepts

* **CRM (Customer Relationship Management)** → System to manage customer interactions
* **HCP (Healthcare Professional)** → Doctors, medical professionals
* **LLM (Large Language Model)** → AI model for understanding language
* **LangGraph** → AI agent framework for tool orchestration

---

## 🛠️ Tech Stack

### Frontend

* React (UI development)
* Redux (State management)
* Axios (API calls)

### Backend

* FastAPI (Python API framework)
* LangGraph (AI agent orchestration)
* Groq LLM (Language model)

---

## ⚙️ Features

### ✅ AI-Controlled Form

* Users do NOT manually fill the form
* AI extracts and fills all fields automatically

### ✅ 5 LangGraph Tools

1. **Log Interaction Tool**

   * Extracts HCP name, date, time, sentiment, topics, materials

2. **Edit Interaction Tool**

   * Updates specific fields only
   * Example: “Change sentiment to negative”

3. **Reset Tool**

   * Clears all form data

4. **Suggest Tool**

   * Generates AI-based follow-up actions

5. **Summarize Tool**

   * Creates summary of interaction

---

## 🔄 System Flow

1. User enters message in chat
2. Frontend sends request to backend (`/chat`)
3. LangGraph agent selects appropriate tool
4. Tool processes input using rules + LLM
5. Backend returns structured response
6. Frontend updates form automatically

---

## 🖥️ UI Layout

* **Left Panel** → Interaction Form
* **Right Panel** → AI Chat Assistant

---

## 🧪 Test Cases

Try these inputs:

```
Met Dr. Smith today at 5pm, discussion went well
Change sentiment to negative
Clear the form
Suggest next steps
Summarize interaction
```

---

## 📦 Installation & Setup

### 🔹 Clone Repository

```
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

---

### 🔹 Frontend Setup

```
cd frontend
npm install
npm start
```

Runs on: `http://localhost:3000`

---

### 🔹 Backend Setup

```
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Runs on: `http://127.0.0.1:8000`

---

## 🔐 Environment Setup

Replace your Groq API key in backend:

```python
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key="YOUR_API_KEY"
)
```

---

## 📁 Project Structure

```
project-root/
 ├── frontend/
 │    ├── src/
 │    ├── public/
 │    ├── package.json
 │
 ├── backend/
 │    ├── main.py
 │    ├── requirements.txt
 │
 ├── README.md
 └── .gitignore
```

---

## 🎥 Video Demonstration

The video includes:

* Frontend walkthrough
* All 5 tools demonstration
* Code explanation
* System architecture

---

## 🚀 Key Highlights

* AI replaces manual form filling
* Real-time structured data extraction
* Modular tool-based architecture
* Scalable using LangGraph

---

## 📌 Conclusion

This project demonstrates how **AI can transform traditional CRM systems** into intelligent, conversational platforms, improving efficiency and user experience.

---

## 👤 Author

**Prashantha R**

---
