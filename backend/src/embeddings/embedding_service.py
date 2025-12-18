from typing import List
from sentence_transformers import SentenceTransformer
from ..config import settings


class EmbeddingService:
    def __init__(self):
        # Load the pre-trained sentence transformer model
        self.model = SentenceTransformer(settings.embedding_model)
        
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        """
        embedding = self.model.encode([text], convert_to_numpy=True)
        # Convert to list for JSON serialization
        return embedding[0].tolist()
        
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts
        """
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        # Convert to list of lists for JSON serialization
        return [embedding.tolist() for embedding in embeddings]
        
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embeddings produced by the model
        """
        # Generate a sample embedding to determine dimensions
        sample_embedding = self.generate_embedding("sample text")
        return len(sample_embedding)


# Global instance of the EmbeddingService
embedding_service = EmbeddingService()