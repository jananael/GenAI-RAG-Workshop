from flask import Blueprint, request, jsonify

from app.rag.retriever import retrieve_context
from app.prompts import build_rag_prompt
from app.llm import call_llama3
from app.rag.loader import load_text_file
from app.rag.chunker import chunk_text
from app.rag.vectorstore import add_documents

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}

    if "question" not in data:
        return jsonify({"error": "Missing 'question' field"}), 400

    question = data["question"].strip()
    if not question:
        return jsonify({"error": "Question is empty"}), 400

    context = retrieve_context(question)  
    prompt = build_rag_prompt(context, question)

    result = call_llama3(prompt)
    return jsonify({"answer": result})


@api_blueprint.route("/upload", methods=["POST"])
def upload_document():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        text = load_text_file(file)
        chunks = chunk_text(text)

        
        add_documents(chunks)

        return jsonify({
            "message": "Document uploaded successfully",
            "chunks_added": len(chunks)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
