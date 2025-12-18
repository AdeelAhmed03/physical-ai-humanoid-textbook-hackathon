from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
import logging

from src.services.content_service import ContentService
from src.services.embedding_search import embedding_search_service
from src.models.chapter import Chapter

router = APIRouter(prefix="/search", tags=["search"])

logger = logging.getLogger(__name__)


class SearchQuery(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = {}
    limit: Optional[int] = 10
    offset: Optional[int] = 0


class SearchResult(BaseModel):
    id: str
    title: str
    content: str
    score: float
    chapter_id: str
    textbook_id: str


class SearchResponse(BaseModel):
    results: List[SearchResult]
    total: int
    query_time_ms: float


@router.post("/", response_model=SearchResponse)
async def search_content(
    search_query: SearchQuery,
    content_service: ContentService = Depends(ContentService)
):
    """
    Search textbook content using semantic search
    """
    try:
        import time
        start_time = time.time()

        # Perform semantic search using embeddings
        search_results = await embedding_search_service.search(
            query=search_query.query,
            filters=search_query.filters,
            limit=search_query.limit,
            offset=search_query.offset
        )

        # Track search event for analytics
        embedding_search_service.track_search_event(
            query=search_query.query,
            results_count=len(search_results['results']),
            user_id=None  # Would come from authentication in real implementation
        )

        # Convert results to the expected format
        results = []
        for result in search_results['results']:
            results.append(SearchResult(
                id=result.get('id'),
                title=result.get('title', ''),
                content=result.get('content', '')[:500],  # Limit content length
                score=result.get('score', 0.0),
                chapter_id=result.get('chapter_id', ''),
                textbook_id=result.get('textbook_id', '')
            ))

        query_time_ms = (time.time() - start_time) * 1000

        return SearchResponse(
            results=results,
            total=search_results.get('total', len(results)),
            query_time_ms=query_time_ms
        )
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")