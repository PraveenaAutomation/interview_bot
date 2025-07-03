from flask import Flask, request, jsonify
from flask_cors import CORS

from backend.langgraph_bot import build_rag_graph

app = Flask(__name__)

# Build the LangGraph app once at startup
qa_bot = build_rag_graph()
# Allow all origins for dev purposes
CORS(app, resources={r"/ask": {"origins": "*"}})
# CORS(app)
@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question is required"}), 400

    try:
        result = qa_bot.invoke({"question": question, "documents": [], "answer": ""})
        return jsonify({"question": question, "answer": result["answer"]})
    except Exception as e:
        return jsonify({
            "error": "Something went wrong while generating the answer.",
            "details": str(e)
        }), 500


@app.route("/", methods=["GET"])
def home():
    return "LangGraph Interview Q&A Bot is running."


if __name__ == "__main__":
    app.run(debug=True)
