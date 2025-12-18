// frontend/api/personalization.js
export default async function handler(req, res) {
  if (req.method !== 'POST' && req.method !== 'GET') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  try {
    if (req.method === 'GET') {
      // Return mock personalized learning path
      const learningPath = {
        userId: '123',
        recommendedChapters: [
          { id: '3', title: 'Advanced Physical AI Concepts', priority: 1 },
          { id: '4', title: 'Humanoid Locomotion', priority: 2 },
          { id: '5', title: 'Sensor Integration', priority: 3 }
        ],
        nextSteps: ['Complete chapter 3', 'Try the simulation exercise', 'Take the quiz']
      };

      return res.status(200).json(learningPath);
    } else if (req.method === 'POST') {
      // Handle personalization updates
      const { userId, preferences } = req.body;
      
      return res.status(200).json({
        message: 'Personalization preferences updated',
        userId: userId,
        preferences: preferences
      });
    }
  } catch (error) {
    console.error('Personalization API Error:', error);
    return res.status(500).json({
      error: 'Personalization service failed',
      message: error.message
    });
  }
}

export const config = {
  api: {
    responseLimit: '10mb',
  },
};