from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv() 

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["Contact_Project"]  


# MONGO_URI=mongodb+srv://Admin:user123@cluster0.8jsoc.mongodb.net

# Database=Contact_Project