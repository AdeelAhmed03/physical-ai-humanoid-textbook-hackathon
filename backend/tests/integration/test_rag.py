"""
Integration test for RAG functionality in backend/tests/integration/test_rag.py
"""
import pytest
from unittest.mock import patch, MagicMock
from src.embeddings import search_similar_content, generate_and_store_embeddings
from src.services.vector_db import vector_db_service


def test_rag_search_functionality():
    """
    Test the RAG search functionality
    """
    # Mock the embedding service to return consistent values
    with patch('src.embeddings.embedding_service') as mock_embedding:
        mock_embedding.generate_embedding.return_value = [0.1, 0.2, 0.3] * 128  # 384-dim vector
        
        # Mock the vector DB service
        with patch('src.embeddings.vector_db_service') as mock_vector_db:
            mock_vector_db.search_similar.return_value = [
                {
                    "id": "test-point-id",
                    "score": 0.9,
                    "payload": {
                        "content_id": "test-content-id",
                        "chapter_id": "intro-physical-ai",
                        "text": "Physical AI combines artificial intelligence with physical systems."
                    }
                }
            ]
            
            # Test the search functionality
            results = search_similar_content("What is Physical AI?", chapter_id="intro-physical-ai", limit=1)
            
            # Verify the results
            assert len(results) == 1
            assert results[0]["payload"]["text"] == "Physical AI combines artificial intelligence with physical systems."
            assert results[0]["score"] == 0.9


def test_generate_and_store_embeddings():
    """
    Test the embedding generation and storage functionality
    """
    # Mock the embedding service
    with patch('src.embeddings.embedding_service') as mock_embedding:
        mock_embedding.generate_embedding.return_value = [0.1, 0.2, 0.3] * 128  # 384-dim vector
        mock_embedding.generate_embeddings_batch.return_value = [[0.1, 0.2, 0.3] * 128]
        
        # Mock the vector DB service
        with patch('src.embeddings.vector_db_service') as mock_vector_db:
            # Test the function
            chapter_id = "test-chapter"
            content = "This is a test content for embedding."
            
            result = generate_and_store_embeddings(chapter_id, content)
            
            # Verify the function returns the number of embeddings created
            assert result == 1  # One chunk was created
            
            # Verify the vector DB service was called
            assert mock_vector_db.add_embeddings_batch.called


def test_rag_service_integration():
    """
    Test the integration between embedding generation, storage, and search
    """
    # This test would normally require a real vector database
    # For integration testing purposes, we'll test the logic flow
    with patch('src.embeddings.embedding_service') as mock_embedding, \
         patch('src.embeddings.content_processor') as mock_processor, \
         patch('src.embeddings.vector_db_service') as mock_vector_db:
        
        # Mock the embedding service
        mock_embedding.generate_embedding.return_value = [0.1, 0.2, 0.3] * 128
        
        # Mock content processor
        mock_processor.process_chapter.return_value = [
            {
                'content_id': 'test-content-id',
                'chapter_id': 'test-chapter',
                'text': 'This is test content.'
            }
        ]
        
        # Mock vector DB
        mock_vector_db.search_similar.return_value = [
            {
                "id": "test-point-id",
                "score": 0.85,
                "payload": {
                    "content_id": "test-content-id",
                    "chapter_id": "test-chapter",
                    "text": "This is test content."
                }
            }
        ]
        
        # Test search functionality
        results = search_similar_content("test query")
        
        # Verify results
        assert len(results) == 1
        assert results[0]["score"] == 0.85