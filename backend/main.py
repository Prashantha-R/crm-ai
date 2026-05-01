from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain.tools import tool
from langchain_groq import ChatGroq
import re
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# =========================
# LOAD ENV
# =========================
load_dotenv()

app = FastAPI()

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# LLM SETUP
# =========================
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY missing")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=api_key
)

# =========================
# MEMORY (simple state)
# =========================
memory = {}

# =========================
# REQUEST MODEL
# =========================
class ChatRequest(BaseModel):
    message: str

# =========================
# STATE TYPE
# =========================
class AgentState(TypedDict):
    message: str
    form_data: dict
    response: str

# =========================
# TOOL 1: LOG INTERACTION
# =========================
@tool
def log_interaction_tool(message: str) -> dict:
    """Extract HCP interaction details such as name, date, time, sentiment, materials, topics, outcomes, and follow-up."""
    
    msg = message.lower()

    # HCP NAME
    name_match = re.search(r"(dr\.?\s+[a-z]+)", msg)
    hcp_name = name_match.group(1).title() if name_match else ""

    # DATE
    today = datetime.today()
    if "today" in msg:
        date = today.strftime("%Y-%m-%d")
    elif "yesterday" in msg:
        date = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        date = ""

    # TIME
    time = ""
    time_match = re.search(r"(\d{1,2})(:\d{2})?\s*(am|pm)", msg)
    if time_match:
        h = int(time_match.group(1))
        m = time_match.group(2) if time_match.group(2) else ":00"
        meridian = time_match.group(3)

        if meridian == "pm" and h != 12:
            h += 12
        if meridian == "am" and h == 12:
            h = 0

        time = f"{str(h).zfill(2)}{m}"
    elif "morning" in msg:
        time = "09:00"
    elif "evening" in msg:
        time = "18:00"

    # SENTIMENT
    if any(w in msg for w in ["good", "great", "well"]):
        sentiment = "positive"
    elif any(w in msg for w in ["bad", "poor"]):
        sentiment = "negative"
    else:
        sentiment = "neutral"

    # MATERIALS
    materials = "brochure" if "brochure" in msg else ""

    # TOPICS
    topics = "product discussion" if "discussion" in msg else ""

    # OUTCOME + FOLLOWUP
    if sentiment == "positive":
        outcomes = "Doctor showed interest"
        followup = "Schedule follow-up meeting"
    else:
        outcomes = "Needs further discussion"
        followup = "Plan next visit"

    return {
        "hcp_name": hcp_name,
        "date": date,
        "time": time,
        "sentiment": sentiment,
        "materials": materials,
        "topics": topics,
        "outcomes": outcomes,
        "followup": followup
    }

# =========================
# TOOL 2: EDIT
# =========================
@tool
def edit_interaction_tool(message: str, current: dict) -> dict:
    """Update specific fields like sentiment without modifying other existing data."""

    msg = message.lower()
    updated = current.copy()

    if "positive" in msg:
        updated["sentiment"] = "positive"
    elif "negative" in msg:
        updated["sentiment"] = "negative"
    elif "neutral" in msg:
        updated["sentiment"] = "neutral"

    return updated

# =========================
# TOOL 3: RESET
# =========================
@tool
def reset_tool() -> dict:
    """Clear all form fields and reset interaction data."""

    return {
        "hcp_name": "",
        "date": "",
        "time": "",
        "sentiment": "",
        "materials": "",
        "topics": "",
        "outcomes": "",
        "followup": ""
    }

# =========================
# TOOL 4: SUGGEST
# =========================
@tool
def suggest_tool(message: str) -> str:
    """Generate AI-based follow-up suggestions for the interaction."""

    prompt = f"Suggest 3 short follow-up actions:\n{message}"
    return llm.invoke(prompt).content

# =========================
# TOOL 5: SUMMARIZE
# =========================
@tool
def summarize_tool(data: dict) -> str:
    """Generate a short summary of the interaction."""

    prompt = f"Summarize in 2 lines:\n{data}"
    return llm.invoke(prompt).content

# =========================
# ROUTER
# =========================
def router(state: AgentState):
    msg = state["message"].lower()

    if "clear" in msg:
        return "reset"
    elif "change" in msg:
        return "edit"
    elif "suggest" in msg:
        return "suggest"
    elif "summarize" in msg:
        return "summarize"
    else:
        return "log"

# =========================
# NODES
# =========================
def log_node(state):
    data = log_interaction_tool.invoke(state["message"])
    return {"form_data": data, "response": "Interaction logged successfully"}

def edit_node(state):
    data = edit_interaction_tool.invoke({
        "message": state["message"],
        "current": state["form_data"]
    })
    return {"form_data": data, "response": "Updated successfully"}

def reset_node(state):
    return {"form_data": reset_tool.invoke({}), "response": "Form cleared"}

def suggest_node(state):
    return {
        "form_data": state["form_data"],
        "response": suggest_tool.invoke(state["message"])
    }

def summarize_node(state):
    return {
        "form_data": state["form_data"],
        "response": summarize_tool.invoke({
            "data": state["form_data"]
        })
    }

# =========================
# GRAPH
# =========================
graph = StateGraph(AgentState)

graph.add_node("log", log_node)
graph.add_node("edit", edit_node)
graph.add_node("reset", reset_node)
graph.add_node("suggest", suggest_node)
graph.add_node("summarize", summarize_node)

graph.set_conditional_entry_point(router)

graph.add_edge("log", END)
graph.add_edge("edit", END)
graph.add_edge("reset", END)
graph.add_edge("suggest", END)
graph.add_edge("summarize", END)

app_graph = graph.compile()

# =========================
# API
# =========================
@app.post("/chat")
def chat(req: ChatRequest):
    global memory

    state = {
        "message": req.message,
        "form_data": memory,
        "response": ""
    }

    result = app_graph.invoke(state)

    if result["form_data"]:
        memory = result["form_data"]

    return result