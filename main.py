from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://text-summarizer-frontend-eta.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str

@app.post("/summarize")
def summarize(input: TextInput):
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": input.text})
    try:
        data = response.json()
        summary = data[0]["summary_text"]
        return {"summary": summary}
    except Exception as e:
        return {"error": "Failed to summarize"}

