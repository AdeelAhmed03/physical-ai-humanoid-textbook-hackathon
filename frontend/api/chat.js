// frontend/api/chat.js
import ServerlessRAGService from '../src/services/serverless-rag';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  try {
    const { query, context, chapter_id, conversation_history } = req.body;

    // Initialize the serverless RAG service
    const ragService = new ServerlessRAGService();

    // Process the query using the serverless RAG service
    const result = await ragService.query(query, context || []);

    return res.status(200).json({
      response: result.response,
      sources: result.sources
    });
  } catch (error) {
    console.error('Chat API Error:', error);
    return res.status(500).json({
      error: 'Chat processing failed',
      message: error.message
    });
  }
}

export const config = {
  api: {
    responseLimit: '10mb',
  },
};