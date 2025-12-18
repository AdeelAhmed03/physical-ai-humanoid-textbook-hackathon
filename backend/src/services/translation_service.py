from typing import Optional
import asyncio
import openai
from ..config import settings
import logging

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        # Initialize OpenAI client for translation
        self.openai_client = None
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
            self.openai_client = openai

    def translate_to_urdu(self, text: str) -> Optional[str]:
        """
        Translate English text to Urdu using OpenAI
        """
        if not text.strip():
            return text

        if not self.openai_client:
            # Fallback if OpenAI is not configured
            return f"[Translation service not configured. Original: {text[:100]}...]"

        try:
            # Use OpenAI to translate the text to Urdu
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional translator. Translate the given English text to Urdu. Respond only with the translated text, nothing else."
                    },
                    {
                        "role": "user",
                        "content": f"Translate the following text to Urdu:\n\n{text}"
                    }
                ],
                max_tokens=len(text) * 2,  # Urdu text is often longer than English
                temperature=0.3
            )

            translated_text = response.choices[0].message.content.strip()
            return translated_text
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text  # Return original text if translation fails

    async def translate_text_async(self, text: str, target_language: str = "ur") -> Optional[str]:
        """
        Asynchronously translate text to target language
        """
        if target_language.lower() != "ur":
            # For now, only Urdu is supported
            return text

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.translate_to_urdu, text)

translation_service = TranslationService()