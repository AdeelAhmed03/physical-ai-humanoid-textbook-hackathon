import uuid
from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from ..config import settings


class VectorDBService:
    def __init__(self):
        # Initialize Qdrant client
        if settings.qdrant_api_key:
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                prefer_grpc=True,
            )
        else:
            self.client = QdrantClient(
                url=settings.qdrant_url,
                prefer_grpc=True,
            )
        
        # Collection name for textbook embeddings
        self.collection_name = "textbook_embeddings"
        
        # Initialize the collection if it doesn't exist
        self._initialize_collection()
    
    def _initialize_collection(self):
        """Initialize the Qdrant collection if it doesn't exist"""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except Exception:
            # Collection doesn't exist, create it
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=settings.embedding_dimensions,
                    distance=Distance.COSINE
                )
            )
            
            # Create payload index for content_id and chapter_id to optimize search
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="content_id",
                field_schema=models.PayloadSchemaType.KEYWORD
            )
            
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="chapter_id",
                field_schema=models.PayloadSchemaType.KEYWORD
            )
    
    def add_embedding(self, content_id: str, chapter_id: str, vector: List[float], text: str):
        """Add a single embedding to the collection"""
        point = models.PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "content_id": content_id,
                "chapter_id": chapter_id,
                "text": text
            }
        )
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
    
    def add_embeddings_batch(self, embeddings_data: List[dict]):
        """Add multiple embeddings to the collection"""
        points = []
        for data in embeddings_data:
            point = models.PointStruct(
                id=str(uuid.uuid4()),
                vector=data["vector"],
                payload={
                    "content_id": data["content_id"],
                    "chapter_id": data["chapter_id"],
                    "text": data["text"]
                }
            )
            points.append(point)
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
    
    def search_similar(self, query_vector: List[float], chapter_id: Optional[str] = None, limit: int = 5) -> List[dict]:
        """Search for similar embeddings to the query vector"""
        # Prepare the search filter if chapter_id is specified
        search_filter = None
        if chapter_id:
            search_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="chapter_id",
                        match=models.MatchValue(value=chapter_id)
                    )
                ]
            )
        
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=search_filter,
            limit=limit,
            with_payload=True
        )
        
        # Format the results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.id,
                "score": result.score,
                "payload": result.payload
            })
        
        return formatted_results
    
    def get_by_content_id(self, content_id: str) -> List[dict]:
        """Retrieve embeddings by content_id"""
        results = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="content_id",
                        match=models.MatchValue(value=content_id)
                    )
                ]
            ),
            limit=1000  # Adjust as needed
        )
        
        formatted_results = []
        for result in results[0]:  # Results are returned as (records, next_page_offset)
            formatted_results.append({
                "id": result.id,
                "payload": result.payload,
                "vector": result.vector
            })
        
        return formatted_results
    
    def delete_by_content_id(self, content_id: str):
        """Delete embeddings by content_id"""
        # Get points with this content_id first
        points_to_delete = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="content_id",
                        match=models.MatchValue(value=content_id)
                    )
                ]
            ),
            limit=10000  # Adjust as needed
        )[0]
        
        # Extract point IDs
        point_ids = [point.id for point in points_to_delete]
        
        if point_ids:
            # Delete the points
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=point_ids
                )
            )
    
    def get_all_chapter_ids(self) -> List[str]:
        """Get all unique chapter IDs in the collection"""
        # Get all points and extract unique chapter IDs
        all_points = self.client.scroll(
            collection_name=self.collection_name,
            limit=10000  # Adjust as needed
        )[0]
        
        chapter_ids = set()
        for point in all_points:
            chapter_id = point.payload.get("chapter_id")
            if chapter_id:
                chapter_ids.add(chapter_id)
        
        return list(chapter_ids)


# Global instance of the VectorDBService
vector_db_service = VectorDBService()