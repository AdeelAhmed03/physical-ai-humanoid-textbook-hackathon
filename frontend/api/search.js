// frontend/api/search.js
export default async function handler(req, res) {
  if (req.method !== 'GET' && req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  try {
    let query = '';
    
    if (req.method === 'GET') {
      query = req.query.q || req.query.query || '';
    } else if (req.method === 'POST') {
      query = req.body.query || req.body.q || '';
    }

    if (!query) {
      return res.status(400).json({ 
        error: 'Query parameter is required' 
      });
    }

    // In a real implementation, this would search a vector database
    // For Vercel serverless, you'd need a hosted solution
    
    // Mock search results
    const searchResults = [
      {
        id: '1',
        title: 'Introduction to Physical AI',
        content: 'Physical AI combines machine learning with physical systems...',
        score: 0.95
      },
      {
        id: '2',
        title: 'Humanoid Robotics',
        content: 'Humanoid robots are robots with human-like form and capabilities...',
        score: 0.87
      },
      {
        id: '3',
        title: 'ROS 2 Fundamentals',
        content: 'Robot Operating System (ROS) is a flexible framework for writing robot software...',
        score: 0.78
      }
    ];

    return res.status(200).json({
      results: searchResults,
      query: query,
      total: searchResults.length
    });
  } catch (error) {
    console.error('Search API Error:', error);
    return res.status(500).json({
      error: 'Search failed',
      message: error.message
    });
  }
}

export const config = {
  api: {
    responseLimit: '10mb',
  },
};