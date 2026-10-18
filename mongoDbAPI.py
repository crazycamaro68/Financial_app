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
    result = collection.find({"date":{"$gte":start_date,"$lt":end_date}}).sort("date")
    return result

def insert_transaction(transaction):
    collection.insert_one({"date":transaction.date, "description":transaction.description,"amount":transaction.amount})

def update_transaction(old_transaction,new_transaction):
    # create a query filter to find the orignal
    to_be_update = {"date":old_transaction.date, "description":old_transaction.description,"amount":old_transaction.amount}
    # create a update operation to set new values
    update_operation = {"$set" : {"date":new_transaction.date, "description":new_transaction.description,"amount":new_transaction.amount}}

    result = collection.update_one(to_be_update, update_operation)
    print(result.matched_count)
    
def remove_transaction(transaction):
    collection.delete_one({"date":transaction.date, "description":transaction.description,"amount":transaction.amount})

