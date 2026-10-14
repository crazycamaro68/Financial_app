import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

mongoURL = os.getenv("MONGO_URL")

client = MongoClient(mongoURL)

db = client["Financial"]
collection = db["Transactions"]

def pull_transactions(start_date, end_date):
    result = collection.find({"date":{"$gte":start_date,"$lt":end_date}})
    return result

test_data = pull_transactions(datetime(2026,8,5),datetime(2026,8,10))
for document in test_data:
    print(document)