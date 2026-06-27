from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.chatbot import ask

app = FastAPI(
    title="ecom-beauty-chatbot",
    version="0.1.0",
    description="A simple ecommerce chatbot API served by uvicorn.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8001",
        "http://127.0.0.1:8001",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "service": "ecom-beauty-chatbot"}


@app.post("/ask", response_model=ChatResponse, tags=["chat"])
def ask_question(request: ChatRequest):
    answer = ask(request.question)
    return ChatResponse(answer=answer)
