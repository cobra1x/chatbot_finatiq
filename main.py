from fastapi import FastAPI
from dotenv import load_dotenv
import os
from sarvamai import SarvamAI
load_dotenv()

sarvam_api_key=os.getenv("SARVAM_API_KEY")
client=SarvamAI(api_subscription_key=sarvam_api_key)
app=FastAPI()

SYSTEM_PROMPT = """You are SubClear AI, an expert Fintech AI Assistant specializing in auto-debit audit and recurring payment discovery.
    Your mission is to process cryptic transaction strings, reveal hidden subscriptions, spot price hikes, and produce actionable step-by-step cancellation instructions.
    Translate technical steps into clear, natural Indic languages (or Hinglish/Tanglish) to make financial audit accessible to everyone.
    Include precise guidance on managing e-Mandates, UPI AutoPay, and card recurring billing."""

from pydantic import BaseModel

class QueryModel(BaseModel):
    inp: str

@app.get('/')
def home():
    return {'message':'server is running'}

@app.post('/answer')
def answer(que:QueryModel):

    response = client.chat.completions(
        model="sarvam-105b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": que.inp
            }
        ],
        temperature=0.3,
        max_tokens=600,
        reasoning_effort=None
    )
    
    return {'message':response.choices[0].message.content}