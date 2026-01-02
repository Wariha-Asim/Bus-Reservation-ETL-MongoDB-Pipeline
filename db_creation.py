from pymongo import MongoClient
import os

# MongoDB connection (set MONGO_URI in environment variables)
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
mongo_client = MongoClient(mongo_uri)

# Database & collection
mdb = mongo_client["BRMSFinal1"]
mongo_col = mdb["brms_denorm"]

print("MongoDB database and collection connected successfully!")
