import os
import uvicorn
from src.main import app

# For Railway deployment, specify the port to use the environment variable
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Railway uses PORT environment variable
    uvicorn.run(app, host="0.0.0.0", port=port)