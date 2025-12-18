// frontend/api/textbook.js
export default async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  try {
    // This would typically fetch from a database in a real implementation
    // For Vercel deployment, you would need to either:
    // 1. Store textbook content as static files in the repo
    // 2. Use a hosted database with API access
    // 3. Use Vercel's KV store or similar for caching
    
    // Mock textbook content response
    const textbookContent = {
      chapters: [
        { id: '1', title: 'Introduction to Physical AI', content: 'Physical AI combines machine learning with physical systems...' },
        { id: '2', title: 'Humanoid Robotics Basics', content: 'Humanoid robots are robots with human-like form and capabilities...' },
        { id: '3', title 'ROS 2 Fundamentals', content: 'Robot Operating System (ROS) is a flexible framework for writing robot software...' }
      ]
    };

    return res.status(200).json(textbookContent);
  } catch (error) {
    console.error('Textbook API Error:', error);
    return res.status(500).json({
      error: 'Failed to fetch textbook content',
      message: error.message
    });
  }
}

export const config = {
  api: {
    responseLimit: '10mb',
  },
};