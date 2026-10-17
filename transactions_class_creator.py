import mongoDbAPI
from datetime import datetime
#Makes all the transactions into objects to be easily handled and modify.
class Transactions:
    instances = []

    def __init__(self, date, description, amount):
        self.date = date
        self.description = description
        self.amount = amount

    def changeDesc(self, newDescription):
        if newDescription:
            self.description = newDescription

    def changeAmount(self, newAmount):
        if newAmount is None:
            raise ValueError("Amount cannot be None.")

        if not isinstance(newAmount, (int, float)):
            raise TypeError("Amount must be a number (int or float).")

        self.amount = newAmount

    # Finds all the Data for the current month and year and stores it in cls.instances
    @classmethod
    def init_data_from_cursor(cls, month, year):
        # Resets instances
        cls.instances = []

        # sets date ranges for current month
        start_date = datetime(year, month, 1)

        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        # retreives data and makes objects with data and stores them in cls.instances
        cursor = mongoDbAPI.pull_transactions(start_date,end_date)
        for transaction in cursor:
            new_transaction = cls(transaction["date"],transaction["description"],transaction["amount"])
            cls.instances.append(new_transaction)
