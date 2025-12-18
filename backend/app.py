import os
from src.main import app

# For Hugging Face Spaces, we just need the FastAPI app
# The Hugging Face runtime will handle the server part
# This format makes it compatible with Hugging Face Spaces
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))  # Hugging Face Spaces uses PORT environment variable
    uvicorn.run(app, host="0.0.0.0", port=port)
else:
    # This is needed for when the app is run in a Hugging Face Space
    # The app variable should be available for the Hugging Face runtime
    pass