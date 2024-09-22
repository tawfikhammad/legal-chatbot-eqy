from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv('.env.example')

def get_database():
    CONNECTION_STRING = 'mongodb+srv://elmetwalleyhammad:uy5ZxY0sFvm6lZ78@cluster0.zupkc.mongodb.net/'
    
    if not CONNECTION_STRING:
        raise ValueError("No MongoDB connection string found in environment variables.")
    
    client = MongoClient(CONNECTION_STRING)
    db = client['legalDocsDB']

    return db

def fetch_documents():
    db = get_database()
    collection = db['legal_pdfs']
    docs = list(collection.find({}, {"pdf_text": 1, "sub_link": 1, "title": 1, "sub_title": 1}))
    
    return docs
