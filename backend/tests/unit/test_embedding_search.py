import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.services.embedding_search import EmbeddingSearchService
from src.services.vector_db import vector_db_service
from src.embeddings.embedding_service import embedding_service


class TestEmbeddingSearchService:
    """Unit tests for EmbeddingSearchService"""
    
    def setup_method(self):
        self.search_service = EmbeddingSearchService()
    
    @patch('src.services.vector_db.vector_db_service.search_similar')
    @patch('src.embeddings.embedding_service.embedding_service.generate_embedding')
    @pytest.mark.asyncio
    async def test_search(self, mock_generate_embedding, mock_search_similar):
        """Test the search method with mocked dependencies"""
        # Setup mocks
        mock_generate_embedding.return_value = [0.1, 0.2, 0.3]
        mock_search_similar.return_value = [
            {
                'id': 'result1',
                'payload': {
                    'title': 'Test Title',
                    'text': 'Test content',
                    'chapter_id': 'chapter1',
                    'textbook_id': 'book1'
                },
                'score': 0.8
            }
        ]
        
        # Call the search method
        result = await self.search_service.search(
            query="test query",
            limit=5
        )
        
        # Verify the result structure
        assert 'results' in result
        assert len(result['results']) == 1
        assert result['results'][0]['title'] == 'Test Title'
        assert 'highlight' in result['results'][0]['content']
        
        # Verify that the mocked methods were called
        mock_generate_embedding.assert_called_once_with("test query")
        mock_search_similar.assert_called_once()
    
    def test_highlight_query_terms(self):
        """Test the highlighting functionality"""
        text = "This is a sample text with some content."
        query = "sample content"
        
        highlighted = self.search_service._highlight_query_terms(text, query)
        
        # Check that the query terms are highlighted
        assert '[highlight]sample[/highlight]' in highlighted
        assert '[highlight]content[/highlight]' in highlighted