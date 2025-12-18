from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
from ..services.rag_service import RAGService
from ..db.session import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/chat", tags=["chat"])

logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    query: str
    context: Optional[List[Dict[str, Any]]] = []
    chapter_id: Optional[str] = None
    conversation_history: Optional[List[Dict[str, str]]] = {}


class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = []


@router.post("/", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Process chat messages using RAG with OpenAI
    """
    try:
        # Initialize RAG service
        rag_service = RAGService()

        # Process the query using the RAG service
        result = rag_service.query(
            question=chat_request.query,
            context=chat_request.context
        )

        return ChatResponse(
            response=result.get("response", "Sorry, I couldn't process your request"),
            sources=result.get("sources", [])
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")