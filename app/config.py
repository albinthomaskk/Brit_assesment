import os
from dotenv import load_dotenv
from pymongo import MongoClient
# Load environment variables from the .env file
load_dotenv()

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
