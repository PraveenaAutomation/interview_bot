import os
import json
from dotenv import load_dotenv
from typing import List, Dict, TypedDict

# LangChain components
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore

# LangGraph components
from langgraph.graph import StateGraph, END

# Import vector store related functions from your backend.vector_store module
from backend.vector_store import load_vector_store, format_docs

# Load environment variables
load_dotenv()

class GraphState(TypedDict):
    question: str
    documents: List[Document]
    answer: str

def retrieve(state: GraphState) -> Dict[str, any]:
    print("---RETRIEVE NODE---")
    question = state["question"]
    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    documents = retriever.invoke(question)
    print(f"Retrieved {len(documents)} documents.")
    for i, doc in enumerate(documents):
        print(f"  Document {i + 1} (page_content preview): {doc.page_content[:100]}...")
    return {"question": question, "documents": documents}

def generate(state: GraphState) -> Dict[str, any]:
    print("---GENERATE NODE---")
    question = state["question"]
    documents = state["documents"]
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use the context to answer the question.If the answer is not in the context, say 'Sorry, I couldn't find the answer in the documents.'Always say 'Thanks for asking!' at the beginning.Context: {context}"),
        ("human", "Question: {question}")
    ])

    formatted_context = format_docs(documents)
    print(f"Formatted context sent to LLM (preview): {formatted_context[:200]}...")

    generation_chain = prompt_template | llm
    response = generation_chain.invoke({"context": formatted_context, "question": question})

    answer = response.content

    if "Sorry, I couldn't find the answer in the documents." in answer:
        print("🟡 Fallback Message Triggered — Answer was NOT found in vector DB")
    else:
        print("🟢 Answer successfully generated using vector DB context")

    return {"answer": answer, "question": question, "documents": documents}

def build_rag_graph():
    workflow = StateGraph(GraphState)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("generate", generate)
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)
    return workflow.compile()

if __name__ == "__main__":
    qa_bot = build_rag_graph()
    print("\n--- LangGraph RAG Bot Ready ---")

    questions = [
        "What is Selenium?",
        "What is API testing?",
        "What is the capital of France?"  # Intentional fallback test
    ]

    for q in questions:
        print(f"\nQuestion: {q}")
        try:
            result = qa_bot.invoke({"question": q, "documents": [], "answer": ""})
            print(f"Answer: {result['answer']}")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please check Pinecone index, dimensions, or API keys.")