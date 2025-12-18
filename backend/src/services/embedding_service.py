from typing import List
from sentence_transformers import SentenceTransformer
from ..config import settings
from ..utils.logging_config import logger


class EmbeddingService:
    def __init__(self):
        # Load the pre-trained sentence transformer model
        logger.info(f"Loading embedding model: {settings.embedding_model}")
        self.model = SentenceTransformer(settings.embedding_model)
        logger.info("Embedding model loaded successfully")
        
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        """
        logger.debug(f"Generating embedding for text: {text[:50]}...")
        embedding = self.model.encode([text], convert_to_numpy=True)
        # Convert to list for JSON serialization
        result = embedding[0].tolist()
        logger.debug(f"Generated embedding with dimension: {len(result)}")
        return result
        
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts
        """
        logger.debug(f"Generating embeddings for {len(texts)} texts")
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        # Convert to list of lists for JSON serialization
        result = [embedding.tolist() for embedding in embeddings]
        logger.debug(f"Generated {len(result)} embeddings")
        return result
        
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embeddings produced by the model
        """
        # Generate a sample embedding to determine dimensions
        sample_embedding = self.generate_embedding("sample text")
        return len(sample_embedding)


# Global instance of the EmbeddingService
embedding_service = EmbeddingService()