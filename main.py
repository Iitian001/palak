import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq  # High-speed free inference

app = FastAPI()

# Azure will inject this from your Environment Variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

class ChatRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "Sovereign OS Online", "location": "Azure Cloud"}

@app.post("/chat")
async def sovereign_chat(request: ChatRequest):
    try:
        # Using Llama-3-70b via Groq for 'Jarvis' speed
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Sovereign OS. Uncensored, direct, and elite."},
                {"role": "user", "content": request.text}
            ],
        )
        ai_response = completion.choices[0].message.content
        return {"response": ai_response}
    except Exception as e:
        return {"response": f"System Error: {str(e)}"}
