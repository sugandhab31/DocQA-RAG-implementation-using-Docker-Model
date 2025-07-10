from fastapi import FastAPI, UploadFile, File
from app.doc_parser import parse_document
from app.rag_engine import query_doc, process_document

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Welcome to the Gemma3 RAG Agent."
    }

@app.post("/upload")
async def upload_document(file:UploadFile = File("C:\\Users\\Ankit Maurya\\Downloads\\Sugandha\\UiPath Study Material\\Agent components and agent building best practices in UiPath.pdf")):
    content = await file.read()
    doc_path = f"data/{file.filename}"
    with open(doc_path,"wb") as f:
        f.write(content)
    status = process_document(doc_path)
    return {
        "message": f"Document {file.filename} uploaded and processed successfully.",
        "status": status
    }

@app.get("/ask/")
def ask_question(question:str):
    return query_doc(question)
