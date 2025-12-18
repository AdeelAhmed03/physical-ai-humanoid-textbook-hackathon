// frontend/api/user.js (handles /api/user for general user operations)
export default async function handler(req, res) {
  if (req.method === 'POST') {
    // Mock user creation/login
    const { email, password } = req.body;
    
    if (!email || !password) {
      return res.status(400).json({ 
        error: 'Email and password are required' 
      });
    }

    // Mock user creation
    const newUser = {
      id: '123',
      email: email,
      name: email.split('@')[0], // Just for demo
      created_at: new Date().toISOString()
    };

    return res.status(201).json(newUser);
  } else if (req.method === 'GET') {
    // Mock user profile
    const user = {
      id: '123',
      name: 'Demo User',
      email: 'demo@example.com',
      preferences: {
        preferred_language: 'en',
        learning_style: 'visual',
        difficulty_level: 'intermediate'
      }
    };

    return res.status(200).json(user);
  } else {
    return res.status(405).json({ message: 'Method not allowed' });
  }
}

export const config = {
  api: {
    responseLimit: '10mb',
  },
};