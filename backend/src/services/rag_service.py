import os
from typing import List, Dict, Any
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import Qdrant
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
import openai

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class RAGService:
    def __init__(self):
        # Initialize OpenAI embedding model
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize OpenAI language model
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize Qdrant vector store (assuming it's running)
        self.qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        
        # We'll initialize the vector store when we have content to work with
        self.vector_store = None
    
    def initialize_vector_store(self, collection_name: str = "textbook_content"):
        """Initialize the Qdrant vector store"""
        try:
            self.vector_store = Qdrant.from_existing_collection(
                collection_name=collection_name,
                url=self.qdrant_url,
                api_key=self.qdrant_api_key,
                embeddings=self.embeddings
            )
            return True
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            return False
    
    def query(self, question: str, context: List[Dict] = None) -> Dict[str, Any]:
        """Process a query using RAG"""
        if not self.vector_store:
            if not self.initialize_vector_store():
                return {
                    "response": "Error: Vector store not available",
                    "sources": []
                }
        
        # Create a retrieval QA chain
        qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 4})  # Retrieve top 4 results
        )
        
        # Prepare the question with context if provided
        if context:
            context_str = " ".join([str(item) for item in context])
            question = f"Context: {context_str}\n\nQuestion: {question}"
        
        try:
            # Get the response
            response = qa.invoke({"query": question})
            
            # Extract sources from the response's metadata
            # Note: The actual method to extract sources depends on the vector store implementation
            sources = []  # Placeholder - would extract from actual response
            
            return {
                "response": response.get("result", response.get("answer", "No answer generated")),
                "sources": sources
            }
        except Exception as e:
            print(f"Error during RAG query: {e}")
            return {
                "response": "I encountered an error processing your request. Please try again.",
                "sources": []
            }
    
    def add_content(self, content: List[Document], collection_name: str = "textbook_content"):
        """Add content to the vector store"""
        try:
            if not self.vector_store:
                # Create new collection if it doesn't exist
                self.vector_store = Qdrant.from_documents(
                    documents=content,
                    embedding=self.embeddings,
                    url=self.qdrant_url,
                    api_key=self.qdrant_api_key,
                    collection_name=collection_name
                )
            else:
                # Add documents to existing collection
                self.vector_store.add_documents(content)
            
            return True
        except Exception as e:
            print(f"Error adding content to vector store: {e}")
            return False