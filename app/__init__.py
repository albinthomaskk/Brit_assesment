from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize the FastAPI app
app = FastAPI()

# MongoDB connection using MongoClient
mongo_uri = os.getenv("MONGODB_URI")  # Get the MongoDB URI from environment variables
client = MongoClient(mongo_uri)  # Use the MongoDB URI from .env file
db = client["fruit_store"]  # Use the 'fruit_store' database

# Set up static files
static_directory = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_directory), name="static")

# Set up Jinja2 templates
template_directory = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=template_directory)

# Dependency injection to provide the database to the routes
def get_db():
    return db
