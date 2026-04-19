from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain.tools import tool
from langchain_groq import ChatGroq
import json
import re
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ UPDATED MODEL (IMPORTANT FIX)
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key = os.getenv("GROQ_API_KEY")
)

# ✅ MEMORY
memory = {}

# =========================
# REQUEST
# =========================
class ChatRequest(BaseModel):
    message: str = ""

# =========================
# STATE
# =========================
class AgentState(TypedDict):
    message: str
    form_data: dict
    response: str


# =========================
# 🔥 TOOL 1: LOG (STABLE)
# =========================
@tool
def log_interaction_tool(message: str) -> dict:
    """Extract CRM interaction data using rule-based logic"""

    msg = message.lower()

    # NAME
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
    time_match = re.search(r"(\d{1,2})(:\d{2})?\s*(am|pm)", msg)
    time = ""

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
    elif "afternoon" in msg:
        time = "15:00"
    elif "evening" in msg:
        time = "18:00"

    # SENTIMENT
    if any(word in msg for word in ["good", "great", "well", "happy", "positive"]):
        sentiment = "positive"
    elif any(word in msg for word in ["bad", "not good", "negative", "poor"]):
        sentiment = "negative"
    else:
        sentiment = "neutral"

    # MATERIALS
    if "brochure" in msg or "sample" in msg:
        materials = "shared"
    else:
        materials = ""

    # TOPICS
    topics_match = re.search(r"discussed\s+(.*)", msg)
    topics = topics_match.group(1) if topics_match else ""

    return {
        "hcp_name": hcp_name,
        "date": date,
        "time": time,
        "sentiment": sentiment,
        "materials": materials,
        "topics": topics
    }


# =========================
# 🔥 TOOL 2: EDIT (FIXED)
# =========================
@tool
def edit_interaction_tool(message: str, current: dict) -> dict:
    """Update only specified fields using rule-based logic"""

    msg = message.lower()
    updated = current.copy()

    # SENTIMENT
    if "positive" in msg:
        updated["sentiment"] = "positive"
    elif "negative" in msg:
        updated["sentiment"] = "negative"
    elif "neutral" in msg:
        updated["sentiment"] = "neutral"

    # NAME
    name_match = re.search(r"(dr\.?\s+[a-z]+)", msg)
    if name_match:
        updated["hcp_name"] = name_match.group(1).title()

    # TIME
    time_match = re.search(r"(\d{1,2})(:\d{2})?\s*(am|pm)", msg)
    if time_match:
        h = int(time_match.group(1))
        m = time_match.group(2) if time_match.group(2) else ":00"
        meridian = time_match.group(3)

        if meridian == "pm" and h != 12:
            h += 12
        if meridian == "am" and h == 12:
            h = 0

        updated["time"] = f"{str(h).zfill(2)}{m}"

    return updated


# =========================
# TOOL 3: RESET
# =========================
@tool
def reset_tool() -> dict:
    """Clear all form fields"""
    return {
        "hcp_name": "",
        "date": "",
        "time": "",
        "sentiment": "",
        "materials": "",
        "topics": ""
    }


# =========================
# TOOL 4: SUGGEST
# =========================
@tool
def suggest_tool(message: str) -> str:
    """Suggest follow-up actions"""
    return llm.invoke(f"Suggest follow-up actions for: {message}").content


# =========================
# TOOL 5: SUMMARIZE
# =========================
@tool
def summarize_tool(data: dict) -> str:
    """Summarize interaction"""
    return llm.invoke(f"Summarize this interaction: {data}").content


# =========================
# ROUTER
# =========================
def router(state: AgentState):
    msg = state["message"].lower()

    if "clear" in msg or "reset" in msg:
        return "reset"
    elif "change" in msg or "update" in msg:
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
    return {"form_data": reset_tool.invoke({}), "response": "Form cleared successfully"}

def suggest_node(state):
    return {
        "form_data": state["form_data"],
        "response": suggest_tool.invoke(state["message"])
    }

def summarize_node(state):
    return {
        "form_data": state["form_data"],
        "response": summarize_tool.invoke({"data": state["form_data"]})
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