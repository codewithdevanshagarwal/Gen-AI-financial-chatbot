from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from openrouter_api import analyze_nlu, generate_response
from utils import build_prompt_with_nlu, build_budget_prompt, build_spending_insight_prompt
import traceback
import logging
import requests

router = APIRouter()

class NLURequest(BaseModel):
    text: str

class GenerateRequest(BaseModel):
    question: str
    persona: Optional[str] = "student"

class BudgetSummaryRequest(BaseModel):
    income: float
    expenses: Dict[str, float]
    savings_goal: float
    currency: Optional[str] = "$"
    persona: Optional[str] = "student"

class SpendingInsightsRequest(BaseModel):
    income: float
    expenses: Dict[str, float]
    goals: List[Dict[str, str]]  # e.g., [{"name": "Emergency Fund", "amount": 1000, "deadline": "2024-12-31"}]
    currency: Optional[str] = "$"
    persona: Optional[str] = "student"

@router.post("/nlu")
async def nlu_analysis(request: NLURequest):
    try:
        result = analyze_nlu(request.text)
        return {"nlu": result}
    except requests.exceptions.Timeout:
        error_msg = "Request to OpenRouter API timed out. Please try again later."
        logging.error(error_msg)
        raise HTTPException(status_code=504, detail=error_msg)
    except requests.exceptions.ConnectionError:
        error_msg = "Connection to OpenRouter API failed. Please check your internet connection."
        logging.error(error_msg)
        raise HTTPException(status_code=503, detail=error_msg)
    except Exception as e:
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate")
async def generate_answer(request: GenerateRequest):
    try:
        nlu_data = analyze_nlu(request.question)
        prompt = build_prompt_with_nlu(request.question, nlu_data, request.persona)
        messages = [{"role": "user", "content": prompt}]
        answer = generate_response(messages)
        return {
            "persona": request.persona,
            "nlu": nlu_data,
            "prompt": prompt,
            "answer": answer
        }
    except Exception as e:
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/budget-summary")
async def budget_summary(request: BudgetSummaryRequest):
    try:
        prompt = build_budget_prompt(request.dict(), request.persona)
        messages = [{"role": "user", "content": prompt}]
        summary = generate_response(messages)
        return {
            "persona": request.persona,
            "prompt": prompt,
            "summary": summary
        }
    except Exception as e:
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/spending-insights")
async def spending_insights(request: SpendingInsightsRequest):
    try:
        prompt = build_spending_insight_prompt(request.dict(), request.persona)
        messages = [{"role": "user", "content": prompt}]
        insights = generate_response(messages)
        return {
            "persona": request.persona,
            "prompt": prompt,
            "insights": insights
        }
    except Exception as e:
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
