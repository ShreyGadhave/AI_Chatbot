from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str

def query_ollama(prompt: str):
    """ Runs Ollama asynchronously for faster responses """
    process = subprocess.Popen(
        ["ollama", "run", "mistral:latest", prompt],  # Using mistral:latest
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    output, error = process.communicate()
    return output.strip() if output else error.strip()

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = query_ollama(request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "AI Chatbot Backend Running"}
