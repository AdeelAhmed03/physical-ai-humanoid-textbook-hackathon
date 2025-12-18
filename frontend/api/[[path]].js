export default async function handler(req, res) {
  // Get the path from the URL
  const { path } = req.query;

  // Default backend URL - this should be updated to your deployed backend URL
  // Examples:
  // Railway: https://your-app-name.up.railway.app
  // Hugging Face Space: https://your-username-huggingface-space-name.hf.space
  // Render: https://your-app-name.onrender.com
  const backendUrl = process.env.BACKEND_URL ||
                    process.env.NEXT_PUBLIC_BACKEND_URL ||
                    'https://your-railway-app-name.up.railway.app'; // Update this to your actual backend URL

  // Construct the full backend URL
  const targetUrl = `${backendUrl}/api/${Array.isArray(path) ? path.join('/') : path}`;

  // Prepare options for the fetch request
  const options = {
    method: req.method,
    headers: {
      'Content-Type': 'application/json',
      // Remove host header to prevent issues
      ...Object.fromEntries(
        Object.entries(req.headers).filter(([key]) =>
          !['host', 'connection', 'accept-encoding'].includes(key.toLowerCase())
        )
      ),
    },
  };

  // Include body for POST, PUT, PATCH requests
  if (req.body && (req.method === 'POST' || req.method === 'PUT' || req.method === 'PATCH')) {
    options.body = JSON.stringify(req.body);
  }

  try {
    // Forward the request to the backend
    const response = await fetch(targetUrl, options);

    // Get response data
    const data = await response.json();

    // Get headers from the backend response
    const responseHeaders = {};
    for (const [key, value] of response.headers.entries()) {
      if (!['content-encoding', 'content-length', 'transfer-encoding', 'connection'].includes(key.toLowerCase())) {
        responseHeaders[key] = value;
      }
    }

    // Return the response from the backend with proper headers
    res.status(response.status).setHeaders(responseHeaders).json(data);
  } catch (error) {
    console.error('API Proxy Error:', error);
    res.status(500).json({
      error: 'Internal Server Error',
      message: 'Failed to connect to backend service',
      details: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
}

export const config = {
  api: {
    responseLimit: '10mb', // Increase limit for large responses
  },
};