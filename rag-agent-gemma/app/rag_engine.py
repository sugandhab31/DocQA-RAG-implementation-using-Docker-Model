from app.doc_parser import parse_document
from app.retriever import split_text, create_vectorstore, retrieve_similar_chunks
from openai import OpenAI

# Set up OpenAI-compatible client for Docker-hosted model
client = OpenAI(
    base_url="http://localhost:12434/v1",  # Adjusted endpoint
    api_key="docker"  # Dummy key (required, even if not used)
)

def process_document(file_path: str) -> str:
    full_text = parse_document(file_path)
    chunks = split_text(full_text)
    status = create_vectorstore(chunks)
    return status

def query_doc(user_question: str) -> dict:
    relevant_chunks = retrieve_similar_chunks(user_question)
    context = "\n\n".join(relevant_chunks)

    prompt = f"""You are a helpful AI assistant. Use the following context to answer the question concisely.

    Context:
    {context}

    Question:
    {user_question}

    Answer:"""

    try:
        completion = client.chat.completions.create(
            model="ai/smollm2",
            messages=[
                {"role": "system", "content": "Answer concisely using the document."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = completion.choices[0].message.content
        return {"answer": answer.strip()}

    except Exception as e:
        return {"error": str(e)}
