// frontend/api/auth/login.js
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({
        error: 'Email and password are required'
      });
    }

    // Mock authentication
    // In a real implementation, you'd validate credentials against a database
    if (email && password) {
      // Generate a mock token
      const token = `mock-jwt-token-for-${email}`;
      
      return res.status(200).json({
        token: token,
        user: {
          id: '123',
          email: email,
          name: email.split('@')[0]
        },
        message: 'Login successful'
      });
    } else {
      return res.status(401).json({
        error: 'Invalid credentials'
      });
    }
  } catch (error) {
    console.error('Auth API Error:', error);
    return res.status(500).json({
      error: 'Authentication failed',
      message: error.message
    });
  }
}

export const config = {
  api: {
    responseLimit: '10mb',
  },
};