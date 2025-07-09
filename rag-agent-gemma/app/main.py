from fastapi import FastAPI, UploadFile, File
from app.doc_parser import parse_document
from app.rag_engine import query_doc

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Welcome to the Gemma3 RAG Agent."
    }

@app.post("/upload")
async def upload_document(file:UploadFile = File("C:\\Users\\Ankit Maurya\\Downloads\\Sugandha\\UiPath Study Material\\UiPath Whitepaper.pdf")):
    content = await file.read()
    doc_path = f"data/{file.filename}"
    with open(doc_path,"wb") as f:
        f.write(content)
    return {
        "message": f"Document {file.filename} uploaded successfully."
    }

@app.get("/ask/")
def ask_question(question:str):
    return query_doc(question)
