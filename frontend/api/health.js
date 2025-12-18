// frontend/api/health.js
export default async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  res.status(200).json({ status: 'healthy', message: 'Backend is running' });
}

export const config = {
  api: {
    responseLimit: '10mb',
  },
};