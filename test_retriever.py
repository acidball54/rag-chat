from app.retriever import retrieve

question = "How long does shipping take?"

documents = retrieve(question)

for index, document in enumerate(documents, start=1):
    print("=" * 60)
    print(f"Chunk {index}")
    print(document.page_content)