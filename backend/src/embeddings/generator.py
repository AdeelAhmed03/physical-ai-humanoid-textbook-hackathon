"""
Embedding generation and storage module
"""
from typing import List, Dict
from ..services.vector_db import vector_db_service
from ..embeddings.embedding_service import embedding_service
from ..utils.logging_config import logger
from ..utils.exceptions import EmbeddingGenerationError


def generate_and_store_embeddings(chapter_id: str, content: str):
    """
    Generate embeddings for a chapter and store them in the vector database
    """
    try:
        logger.info(f"Starting embedding generation for chapter: {chapter_id}")
        
        # Process the content into chunks using our content processor
        from .content_processor import content_processor
        processed_chunks = content_processor.process_chapter(chapter_id, content)
        
        # Prepare data for batch embedding
        embeddings_data = []
        
        for chunk in processed_chunks:
            # Generate embedding for the text
            embedding_vector = embedding_service.generate_embedding(chunk['text'])
            
            # Add to the batch data
            embeddings_data.append({
                'content_id': chunk['content_id'],
                'chapter_id': chunk['chapter_id'],
                'vector': embedding_vector,
                'text': chunk['text']
            })
        
        # Store the embeddings in the vector database
        vector_db_service.add_embeddings_batch(embeddings_data)
        
        logger.info(f"Successfully generated and stored {len(embeddings_data)} embeddings for chapter: {chapter_id}")
        
        return len(embeddings_data)  # Return the number of embeddings created
    except Exception as e:
        logger.error(f"Error generating embeddings for chapter {chapter_id}: {str(e)}", exc_info=True)
        raise EmbeddingGenerationError(f"Failed to generate embeddings for chapter {chapter_id}: {str(e)}", original_error=e)


def generate_single_embedding(text: str) -> List[float]:
    """
    Generate a single embedding for the given text
    """
    try:
        logger.debug(f"Generating embedding for text: {text[:50]}...")
        embedding = embedding_service.generate_embedding(text)
        logger.debug(f"Generated embedding with dimension: {len(embedding)}")
        return embedding
    except Exception as e:
        logger.error(f"Error generating embedding: {str(e)}", exc_info=True)
        raise EmbeddingGenerationError(f"Failed to generate embedding: {str(e)}", original_error=e)


def batch_generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a batch of texts
    """
    try:
        logger.debug(f"Generating embeddings for {len(texts)} texts")
        embeddings = embedding_service.generate_embeddings_batch(texts)
        logger.debug(f"Generated {len(embeddings)} embeddings")
        return embeddings
    except Exception as e:
        logger.error(f"Error generating batch embeddings: {str(e)}", exc_info=True)
        raise EmbeddingGenerationError(f"Failed to generate batch embeddings: {str(e)}", original_error=e)