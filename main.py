from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os

# .env se key load karo
load_dotenv()

# Naya Gemini client — google.genai package
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Tumhara app
app = FastAPI()

# Request format
class TransactionRequest(BaseModel):
    amount: float
    recipient: str
    time: str
    method: str

@app.post("/analyze-transaction")
async def analyze_transaction(transaction: TransactionRequest):

    prompt = f"""You are a fraud detection expert for Indian digital payments.

Analyze this transaction and explain in simple Hinglish (Hindi + English mix).
Be direct and clear like you are warning a family member.

Transaction details:
- Amount: ₹{transaction.amount}
- Recipient: {transaction.recipient}
- Time: {transaction.time}
- Payment method: {transaction.method}

Give exactly this format:
VERDICT: SAFE ya SUSPICIOUS

REASON: (2-3 lines Hinglish mein)

ACTION: (1 line — kya karna chahiye abhi)
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return {
        "verdict": response.text,
        "transaction": transaction.model_dump()
    }

@app.get("/")
async def root():
    return {"message": "FinShield AI is running! 🛡️"}