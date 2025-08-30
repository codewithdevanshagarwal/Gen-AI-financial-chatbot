# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import requests
from dotenv import load_dotenv
import os
import uvicorn

# ------------------ LOAD ENV ------------------
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "gpt-4o-mini"  # or gpt-3.5-turbo equivalent

# ------------------ FASTAPI APP ------------------
app = FastAPI(title="Personal Finance Chatbot API")

# ------------------ MODELS ------------------
class Goal(BaseModel):
    name: str
    amount: float

class UserQuery(BaseModel):
    question: str
    persona: Optional[str] = "student"

class BudgetData(BaseModel):
    income: float
    savings_goal: float
    expenses: dict
    persona: Optional[str] = "student"

class SpendingData(BaseModel):
    income: float
    expenses: dict
    goals: List[Goal]
    persona: Optional[str] = "student"

class NLUData(BaseModel):
    text: str

# ------------------ HELPER: CALL OPENROUTER ------------------
def generate_response_ai(prompt: str) -> str:
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    json_data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 500
    }
    try:
        response = requests.post(API_URL, headers=headers, json=json_data, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Failed to generate response: {e}"

# ------------------ ROUTES ------------------
@app.post("/generate")
async def generate(query: UserQuery):
    prompt = (
        f"You are a personal finance advisor for a {query.persona}. "
        f"Answer in a detailed, structured, helpful way with tips and examples.\n\n"
        f"Question: {query.question}"
    )
    answer = generate_response_ai(prompt)
    return {"answer": answer}

@app.post("/budget-summary")
async def budget_summary(data: BudgetData):
    prompt = (
        f"You are a personal finance advisor for a {data.persona}. "
        f"Provide a detailed monthly budget summary including analysis, suggestions, and tips.\n\n"
        f"Income: {data.income}\nSavings Goal: {data.savings_goal}\nExpenses: {data.expenses}"
    )
    summary = generate_response_ai(prompt)
    return {"message": summary}

@app.post("/spending-insights")
async def spending_insights(data: SpendingData):
    goals_text = "\n".join([f"{g.name}: {g.amount}" for g in data.goals])
    prompt = (
        f"You are a personal finance advisor for a {data.persona}. "
        f"Provide detailed spending insights, savings advice, and goal planning.\n\n"
        f"Income: {data.income}\nExpenses: {data.expenses}\nGoals:\n{goals_text}"
    )
    insights = generate_response_ai(prompt)
    return {"message": insights}

@app.post("/nlu")
async def nlu_analysis(data: NLUData):
    prompt = (
        f"Perform a simple natural language analysis.\n"
        f"Provide sentiment (positive/neutral/negative), extract keywords, and identify entities.\n\n"
        f"Text: {data.text}"
    )
    analysis = generate_response_ai(prompt)
    return {"nlu": {"analysis": analysis}}

# ------------------ RUN ------------------
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
#PS C:\Users\adam\OneDrive\Desktop\personal-finance-chatbot\backend> & c:/Users/adam/OneDrive/Desktop/personal-finance-chatbot/backend/.venv_backend/Scripts/Activate.ps1
#(.venv_backend) PS C:\Users\adam\OneDrive\Desktop\personal-finance-chatbot\backend> uvicorn main:app --reload --host 127.0.0.1 --port 8000
               