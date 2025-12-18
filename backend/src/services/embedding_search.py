"""
Embedding search functionality for semantic queries
"""
from typing import List, Optional, Dict, Any
from ..services.vector_db import vector_db_service
from ..embeddings.embedding_service import embedding_service
from ..utils.logging_config import logger
from ..utils.exceptions import RAGProcessingError


class EmbeddingSearchService:
    """
    Service for performing embedding-based semantic searches
    """
    
    def __init__(self):
        pass

    async def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Perform semantic search across textbook content
        """
        try:
            logger.info(f"Performing semantic search for query: {query[:50]}...")

            # Generate embedding for the query
            query_embedding = embedding_service.generate_embedding(query)

            # Apply filters if provided
            chapter_id = None
            if filters:
                chapter_id = filters.get('chapter_id')
            
            # Search in the vector database
            search_results = vector_db_service.search_similar(
                query_vector=query_embedding,
                chapter_id=chapter_id,
                limit=limit,
                offset=offset
            )

            # Format results
            formatted_results = []
            for result in search_results:
                formatted_result = {
                    'id': result.get('id', ''),
                    'title': result.get('payload', {}).get('title', 'Untitled'),
                    'content': self._highlight_query_terms(
                        result.get('payload', {}).get('text', ''),
                        query
                    ),
                    'score': result.get('score', 0.0),
                    'chapter_id': result.get('payload', {}).get('chapter_id', ''),
                    'textbook_id': result.get('payload', {}).get('textbook_id', ''),
                }
                formatted_results.append(formatted_result)

            logger.info(f"Found {len(formatted_results)} results for query")

            return {
                'results': formatted_results,
                'total': len(formatted_results),
                'query': query,
                'filters': filters or {}
            }
        except Exception as e:
            logger.error(f"Error in semantic search: {str(e)}", exc_info=True)
            raise RAGProcessingError(f"Failed to perform semantic search: {str(e)}", original_error=e)

    def _highlight_query_terms(self, text: str, query: str) -> str:
        """
        Highlight query terms in the search result text
        This is a basic implementation that wraps query terms in <mark> tags
        """
        import re
        
        # For simplicity, we'll highlight query terms by wrapping them in [highlight] tags
        # In a real implementation, we might use HTML <mark> tags or other highlighting method
        # that's compatible with the frontend
        query_words = query.lower().split()
        
        highlighted_text = text
        for word in query_words:
            # Use regex to match the word case-insensitively
            pattern = r'\b(' + re.escape(word) + r')\b'
            highlighted_text = re.sub(pattern, r'[highlight]\1[/highlight]', highlighted_text, flags=re.IGNORECASE)
        
        return highlighted_text

    def track_search_event(self, query: str, results_count: int, user_id: Optional[str] = None):
        """
        Track search analytics for performance and user behavior insights
        """
        logger.info(f"Search analytics - Query: {query[:30]}, Results: {results_count}, User: {user_id}")
        # In a real implementation, this would store analytics data to a database or analytics service
        # For now, we just log it
        pass


# Global instance of the EmbeddingSearchService
embedding_search_service = EmbeddingSearchService()