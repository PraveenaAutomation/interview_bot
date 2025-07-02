import os
import json
from dotenv import load_dotenv

# Import Pinecone and OpenAI for LangChain
from pinecone import Pinecone, PodSpec # Import Pinecone for direct initialization if needed, though LangChain handles most of it
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore

# Load environment variables from .env file
load_dotenv()


def format_docs(docs):
    """
    Formats a list of LangChain Document objects into a single string,
    joining their page_content with double newlines.
    This is used to provide context to the LLM.
    """
    return "\n\n".join(doc.page_content for doc in docs)

def load_vector_store():
    """
    Initializes and returns a PineconeVectorStore instance.
    It uses OpenAIEmbeddings for embedding and connects to the Pinecone index
    specified by the INDEX_NAME environment variable.
    """
    embeddings = OpenAIEmbeddings()
    index_name = os.environ["INDEX_NAME"]
    pinecone_api_key = os.environ["PINECONE_API_KEY"]

    vectorstore = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings,
        pinecone_api_key=pinecone_api_key
    )
    return vectorstore

def get_rag_chain():
    """
    Constructs and returns a custom RAG (Retrieval Augmented Generation) chain.
    This chain:
    1. Retrieves relevant documents from Pinecone based on the user's question.
    2. Formats these documents into a single context string.
    3. Combines the context and the original question into a custom prompt.
    4. Passes the prompt to a ChatOpenAI LLM to generate the answer.
    """
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0) # Using a specific model and low temperature for factual answers
    vectorstore = load_vector_store()

    # Define a custom prompt template for RAG
    template = """You are a helpful assistant. Answer the question based on the following context:
{context}

Always say \"Thanks for asking!\" at the beginning of your response.
Question: {question}

Helpful answer:
"""
    custom_rag_prompt = PromptTemplate.from_template(template=template)

    # Construct the RAG chain using LangChain's Runnable interface
    rag_chain = (
        {"context": vectorstore.as_retriever() | format_docs, # Retrieve docs and format them
         "question": RunnablePassthrough()} # Pass the original question through
        | custom_rag_prompt # Apply the custom prompt
        | llm # Pass the prompt to the LLM
    )
    return rag_chain

def save_to_pinecone():
    """
    Loads Q&A data from 'qa_data.json', formats it into LangChain Document objects,
    and then indexes these documents into the specified Pinecone index.
    """
    embeddings = OpenAIEmbeddings()
    index_name = os.environ["INDEX_NAME"]
    pinecone_api_key = os.environ["PINECONE_API_KEY"]

    # Initialize Pinecone client (important for `from_documents` to connect)
    pc = Pinecone(api_key=pinecone_api_key)

    # Load data from qa_data.json
    try:
        with open("qa_data.json", "r", encoding="utf-8") as f:
            qa_data = json.load(f)
    except FileNotFoundError:
        print("Error: qa_data.json not found. Please create it with your Q&A data.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode qa_data.json. Ensure it's valid JSON.")
        return

    # Format documents: one document per Q&A pair
    documents = [
        Document(page_content=f"Q: {item['question']}\nA: {item['answer']}")
        for item in qa_data
    ]

    # Save to Pinecone (will create the index if it doesn't exist)
    print(f"Indexing {len(documents)} documents into Pinecone index: {index_name}...")
    vectorstore = PineconeVectorStore.from_documents(
        documents=documents,
        embedding=embeddings,
        index_name=index_name,
        pinecone_api_key=pinecone_api_key
    )

    print(f"✅ Successfully indexed {len(documents)} documents into Pinecone.")

if __name__ == "__main__":
    # First, populate your Pinecone index with data
    save_to_pinecone()

    # Then, you can use the RAG chain to answer questions
    print("\n--- Testing the RAG Chain ---")
    rag_chain = get_rag_chain()

    # Example query
    question = "What is the capital of France?"
    print(f"\nQuestion: {question}")
    try:
        response = rag_chain.invoke(question)
        print(f"Answer: {response.content}")
    except Exception as e:
        print(f"An error occurred during RAG chain invocation: {e}")
        print("Please ensure your Pinecone index is populated and API keys are correct.")

    question_2 = "Who invented the lightbulb?"
    print(f"\nQuestion: {question_2}")
    try:
        response_2 = rag_chain.invoke(question_2)
        print(f"Answer: {response_2.content}")
    except Exception as e:
        print(f"An error occurred during RAG chain invocation: {e}")

