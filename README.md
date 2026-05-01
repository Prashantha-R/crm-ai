# 🤖 AI-First CRM HCP Interaction System

---

## 📌 Overview

This project is an **AI-first Customer Relationship Management (CRM)** system designed for logging interactions with **Healthcare Professionals (HCPs)** such as doctors.

Instead of manually filling forms, users interact with an **AI Assistant**, which converts **unstructured natural language input into structured CRM data automatically**.

---

## 🎯 Objective

To build an intelligent interaction logging system where:

* Users describe interactions in natural language
* AI extracts structured information
* Form is auto-filled without manual input

👉 This system transforms **unstructured text → structured CRM data in real time**

---

## 🧠 Key Concepts

* **CRM (Customer Relationship Management)** → System to manage interactions with customers
* **HCP (Healthcare Professional)** → Doctors, medical practitioners
* **LLM (Large Language Model)** → AI model used for understanding and generating text
* **LangGraph** → Framework to build AI agents with tool-based workflows

---

## 🛠️ Tech Stack

### 🔹 Frontend

* React (UI development)
* Redux (State management)
* Axios (API communication)

### 🔹 Backend

* FastAPI (Python backend framework)
* LangGraph (AI agent orchestration)
* Groq LLM (Language processing)

---

## ⚙️ Core Features

### ✅ AI-Controlled Form

* No manual data entry
* AI fills form fields automatically

---

### ✅ Unstructured → Structured Conversion

Example input:

Met Dr Ramesh yesterday evening and shared brochure

Converted into:

* HCP Name → Dr Ramesh
* Date → 2026-04-29
* Time → 18:00
* Materials → brochure

---

### ✅ 5 LangGraph Tools

#### 1. Log Interaction Tool

* Extracts structured data from natural language

#### 2. Edit Interaction Tool

* Updates specific fields only
* Example: Change sentiment to negative

#### 3. Reset Tool

* Clears all form data

#### 4. Suggest Tool

* Uses LLM to generate follow-up actions

#### 5. Summarize Tool

* Converts form data into summary text

---

### ⭐ AI Suggested Follow-ups (New Feature)

* Automatically generates actionable next steps
* Displayed as bullet list in UI

Example:

* Schedule follow-up meeting
* Share additional materials
* Confirm next visit

---

## 🔄 System Architecture

### Flow:

1. User enters message in chat
2. Frontend sends request to backend (`/chat`)
3. LangGraph agent acts as decision engine
4. Router selects appropriate tool
5. Tool processes input (rules + LLM)
6. Structured response returned
7. Frontend updates form

👉 AI fully controls the system — user does not manually edit the form

---

## 🖥️ UI Layout

* **Left Panel** → Interaction Form
* **Right Panel** → AI Assistant Chat

Includes:

* Chat bubbles
* Sentiment emojis 😊 😐 😠
* AI Suggested Follow-ups

---

## 🧪 Test Inputs

Try these:

Met Dr Smith today at 5pm, discussion went well
Change sentiment to negative
Suggest next steps
Summarize interaction
Clear the form

---

## 📦 Installation & Setup

### 🔹 Clone Repository

git clone https://github.com/Prashantha-R/crm-ai.git
cd crm-ai

---

### 🔹 Frontend Setup

cd frontend
npm install
npm start

Runs on: http://localhost:3000

---

### 🔹 Backend Setup

cd backend
pip install -r requirements.txt
uvicorn main:app --reload

Runs on: http://127.0.0.1:8000

---

## 🔐 Environment Variables (IMPORTANT)

Create a `.env` file inside `backend/`:

GROQ_API_KEY=your_api_key_here

⚠️ Do NOT upload `.env` to GitHub

---

## 📁 Project Structure

crm-ai/
├── frontend/
│    ├── src/
│    ├── public/
│    ├── package.json
│
├── backend/
│    ├── main.py
│    ├── requirements.txt
│    ├── .env
│
├── README.md
└── .gitignore

---

## 🎥 Video Demonstration

The video includes:

* Frontend walkthrough
* Demonstration of all 5 tools
* AI Suggested Follow-ups
* Code explanation (frontend + backend)
* LangGraph architecture
* Final understanding

---

## 🚀 Key Highlights

* Converts natural language into structured CRM data
* Reduces manual data entry
* Uses AI + rule-based hybrid approach
* Modular architecture using LangGraph
* Scalable and extendable

---

## 📌 Conclusion

This project demonstrates how **AI can replace traditional form-based CRM systems** with conversational interfaces.

It improves:

* Efficiency
* Accuracy
* User experience

---

## 👤 Author

**Prashantha R**
