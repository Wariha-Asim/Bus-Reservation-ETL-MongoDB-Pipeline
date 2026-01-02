from pymongo import MongoClient

# Connection
mongo_client = MongoClient("mongodb://localhost:27017/")

# Database
mdb = mongo_client["BRMSFinal1"]  

# Collection
mongo_col = mdb["brms_denorm"]  

# Test insert
mongo_col.insert_one({
    "test": "This is a test document"
})

print("MongoDB database and collection created successfully!")
