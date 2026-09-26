import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

mongoURL = os.getenv("MONGO_URL")

client = MongoClient(mongoURL)

db = client["Financial"]
collection = db["Transactions"]
# preforms a query on the collection bewteen a date range and returns a cursor. Remeber to use a for loop over the cursor to access the data.
def pull_transactions(start_date, end_date):
    result = collection.find({"date":{"$gte":start_date,"$lte":end_date}})
    return result

