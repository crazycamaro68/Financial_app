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
    
# Currently finds transaction using the date and desc, but amount does not work due to different values bewteen treeview and mongodb
def remove_transaction(transaction):
    collection.delete_one({"date":transaction[0],"description":transaction[1]})

