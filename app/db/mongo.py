from pymongo import MongoClient
from app.core.config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

'''
# Set up the MongoDB client and collection
client = MongoClient(str(MONGO_URI))
db = client[str(DATABASE_NAME)]
collection = db[str(COLLECTION_NAME)]

'''

# Set up the MongoDB client and collection
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]
