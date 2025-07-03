from flask import Flask, request, jsonify
from flask_cors import CORS # Import Flask-CORS

from backend.langgraph_bot import build_rag_graph

app = Flask(__name__)

# Initialize CORS for the entire application
# This allows requests from any origin during development.
# For production, you should restrict 'origins' to your frontend's domain(s).
CORS(app)

# Build the LangGraph app once at startup
try:
    qa_bot = build_rag_graph()
    print("LangGraph RAG Bot initialized successfully for Flask app.")
except Exception as e:
    print(f"Error initializing LangGraph RAG Bot: {e}")
    qa_bot = None # Set to None if initialization fails, to prevent further errors

@app.route("/ask", methods=["POST"])
def ask_question():
    """
    API endpoint to ask a question to the RAG bot.
    Expects a JSON payload with a 'question' field.
    Example:
    {
        "question": "What is Selenium?"
    }
    """
    if qa_bot is None:
        return jsonify({"error": "RAG Bot is not initialized. Check server logs for errors."}), 500

    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Invalid request. Please provide a 'question' in the JSON body."}), 400

    question = data['question']
    print(f"Received question: {question}")

    try:
        # Invoke the LangGraph bot
        # The initial state needs 'question', 'documents' (empty list), and 'answer' (empty string)
        result = qa_bot.invoke({"question": question, "documents": [], "answer": ""})
        answer = result.get('answer', "Could not generate an answer.")
        print(f"Generated answer: {answer}")
        return jsonify({"question": question, "answer": answer})
    except Exception as e:
        print(f"Error during bot invocation: {e}")
        return jsonify({
            "error": "An error occurred while processing your request.",
            "details": str(e)
        }), 500

@app.route("/", methods=["GET"])
def home():
    """
    A simple home route to confirm the Flask app is running.
    """
    return "LangGraph Interview Q&A Bot is running."

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000) # Run on 0.0.0.0 to be accessible from other devices/containers
