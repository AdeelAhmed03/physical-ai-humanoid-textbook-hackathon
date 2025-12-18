"""
Main module for handling embeddings generation and management
"""
from .embedding_service import embedding_service
from .content_processor import content_processor
from ..services.vector_db import vector_db_service


def generate_and_store_embeddings(chapter_id: str, content: str):
    """
    Generate embeddings for a chapter and store them in the vector database
    """
    # Process the content into chunks
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
    
    return len(embeddings_data)  # Return the number of embeddings created


def search_similar_content(query: str, chapter_id: str = None, limit: int = 5):
    """
    Search for content similar to the query
    """
    # Generate embedding for the query
    query_embedding = embedding_service.generate_embedding(query)
    
    # Search in the vector database
    results = vector_db_service.search_similar(
        query_vector=query_embedding,
        chapter_id=chapter_id,
        limit=limit
    )
    
    return results