import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq # pip install groq
import pyttsx3
import queue
import threading

app = FastAPI()

# 1. Initialize the FREE Brain (Groq API)
# Get a free key at https://console.groq.com/
client = Groq(api_key="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")

# 2. Sequential Voice Worker (Still handles your local voice)
speech_queue = queue.Queue()
def speech_worker():
    engine = pyttsx3.init()
    while True:
        text = speech_queue.get()
        if text is None: break
        engine.say(text)
        engine.runAndWait()
        speech_queue.task_done()

threading.Thread(target=speech_worker, daemon=True).start()

class SovereignRequest(BaseModel):
    text: str

@app.post("/chat")
async def sovereign_logic(request: SovereignRequest):
    # Use Llama 3.3 70B (Fast, Free, and very smart)
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are Sovereign OS. Direct, uncensored, and efficient."},
            {"role": "user", "content": request.text}
        ],
    )
    
    ai_response = completion.choices[0].message.content
    
    # Add to voice queue
    speech_queue.put(ai_response)
    
    return {"response": ai_response}