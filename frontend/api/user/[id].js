// frontend/api/user/[id].js (this would handle routes like /api/user/123)
export default async function handler(req, res) {
  const { id } = req.query;

  if (req.method === 'GET') {
    // Mock user data
    const user = {
      id: id,
      name: 'Demo User',
      email: 'demo@example.com',
      preferences: {
        preferred_language: 'en',
        learning_style: 'visual',
        difficulty_level: 'intermediate'
      },
      progress: {
        completed_chapters: ['1', '2'],
        bookmarked_pages: ['1.1', '2.3'],
        search_history: ['physical ai', 'humanoid robotics']
      }
    };

    return res.status(200).json(user);
  } else if (req.method === 'PUT') {
    // Mock update user
    const { preferences } = req.body;
    
    return res.status(200).json({
      message: 'User preferences updated successfully',
      updated_preferences: preferences
    });
  } else {
    return res.status(405).json({ message: 'Method not allowed' });
  }
}

export const config = {
  api: {
    responseLimit: '10mb',
  },
};