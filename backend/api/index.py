# backend/api/index.py
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mangum import Mangum
from src.main import app

# Create the Mangum adapter for ASGI to serverless compatibility
handler = Mangum(app, lifespan="off")

def lambda_handler(event, context):
    return handler(event, context)