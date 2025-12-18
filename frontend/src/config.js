// Environment configuration for frontend
// Since Docusaurus is a static site generator, we handle environment differently
// This file provides a way to manage environment-specific settings

const config = {
  // API endpoints
  // In production, this should point to the Vercel API proxy at /api
  // In development, it might point to the backend server directly
  API_BASE_URL: process.env.REACT_APP_BACKEND_URL ||
                (typeof window !== 'undefined' && window.location.hostname !== 'localhost'
                  ? '/api'
                  : 'http://localhost:8000'),

  // Feature flags
  ENABLE_CHATBOT: process.env.REACT_APP_ENABLE_CHATBOT !== 'false',
  ENABLE_SEARCH: process.env.REACT_APP_ENABLE_SEARCH !== 'false',
  ENABLE_PERSONALIZATION: process.env.REACT_APP_ENABLE_PERSONALIZATION !== 'false',

  // Third-party integrations
  ENABLE_URDU_TRANSLATION: process.env.REACT_APP_ENABLE_URDU !== 'false',

  // Debug settings
  DEBUG: process.env.NODE_ENV === 'development',
};

export default config;