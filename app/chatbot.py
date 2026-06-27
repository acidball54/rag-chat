from langchain_groq import ChatGroq

from app.config import (
    GROQ_API_KEY,
    LLM_MODEL,
)

from app.prompt import SYSTEM_PROMPT

from app.retriever import retrieve


llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=LLM_MODEL,
)


def ask(question: str):

    docs = retrieve(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = SYSTEM_PROMPT.format(
        context=context,
        question=question,
    )

    response = llm.invoke(prompt)

    return response.content