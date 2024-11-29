import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Fetch environment variables
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")