import re
from typing import List, Dict, Optional
from ..config import settings


class ContentProcessor:
    """
    Processes textbook content into chunks suitable for embedding and search indexing
    """

    def __init__(self):
        pass

    def chunk_text(self, text: str, max_length: int = settings.max_content_length) -> List[str]:
        """
        Split text into chunks of specified max length, trying to preserve sentence boundaries
        """
        # Split text into sentences using sentence-ending punctuation
        sentences = re.split(r'[.!?]+\s+', text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            # If adding the current sentence would exceed the max length
            if len(current_chunk) + len(sentence) + 1 > max_length:
                # If the current chunk is not empty, save it
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""

                # If the sentence itself is longer than max_length, split it
                if len(sentence) > max_length:
                    # Split the long sentence into smaller parts
                    sentence_chunks = self._split_long_sentence(sentence, max_length)
                    chunks.extend(sentence_chunks)
                else:
                    # Otherwise, start a new chunk with the current sentence
                    current_chunk = sentence
            else:
                # Add the sentence to the current chunk
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence

        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def _split_long_sentence(self, sentence: str, max_length: int) -> List[str]:
        """
        Split a sentence that is longer than max_length into smaller parts
        """
        if len(sentence) <= max_length:
            return [sentence]

        words = sentence.split()
        chunks = []
        current_chunk = ""

        for word in words:
            if len(current_chunk) + len(word) + 1 <= max_length:
                if current_chunk:
                    current_chunk += " " + word
                else:
                    current_chunk = word
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = word

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def process_chapter(self, chapter_id: str, content: str, chapter_title: str = "", textbook_id: str = "") -> List[Dict]:
        """
        Process a chapter into chunks suitable for embedding and search indexing
        Returns a list of dictionaries with content_id, chapter_id, textbook_id, title, and text
        """
        # Chunk the content
        chunks = self.chunk_text(content)

        processed_chunks = []
        for i, chunk in enumerate(chunks):
            chunk_info = {
                'content_id': f"{chapter_id}_chunk_{i}",
                'chapter_id': chapter_id,
                'textbook_id': textbook_id,
                'title': f"{chapter_title} - Part {i+1}" if chapter_title else f"Chapter {chapter_id} - Part {i+1}",
                'text': chunk,
                'metadata': {
                    'chapter_order': i,
                    'chunk_number': i,
                    'word_count': len(chunk.split()),
                    'textbook_id': textbook_id,
                    'chapter_id': chapter_id
                }
            }
            processed_chunks.append(chunk_info)

        return processed_chunks

    def preprocess_for_search(self, text: str) -> str:
        """
        Preprocess text for search indexing, including cleaning and normalization
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        # Convert to lowercase for basic full-text search
        text = text.lower()

        # Remove special characters if needed for specific search implementation
        # (keeping this simple for now, but could be expanded)

        return text.strip()


# Global instance of the ContentProcessor
content_processor = ContentProcessor()