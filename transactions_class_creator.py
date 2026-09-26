import pandas as pd
import mongoDbAPI
from datetime import datetime
#Makes all the transactions into objects to be easily handled and modify.
class Transactions:
    instances = []
    #df = pd.read_excel("master_transaction.xlsx", sheet_name=1, parse_dates=["Date"])
    #current_date = datetime.now()

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

    def to_dict(self):
        return {
            "Date": self.date,
            "Time": self.time,
            "Description": self.description,
            "Amount": self.amount,
            "Balance": self.balance
        }
    #Validates the data and comfirms it is right datatype before creating Transaction classes and appending them to instance list.
    @classmethod
    def load_from_dataframe(cls, month=None, year=None):
        if month is None:
            month = cls.current_date.month
        if year is None:
            year = cls.current_date.year

        cls.instances.clear()

        filtered_df = cls.df[(cls.df["Date"].dt.month == month) & (cls.df["Date"].dt.year == year)]

        for _, row in filtered_df.iterrows():
            date = pd.to_datetime(row["Date"])
            time = datetime.strftime(pd.to_datetime(row["Time"]),"%H:%M")
            transaction = cls(date, time, row["Description"], row["Amount"], row["Balance"])
            cls.instances.append(transaction)

    @classmethod
    def byMonth(cls, month, year):
        return [t for t in cls.instances if t.date.month == month and t.date.year == year]

    @classmethod
    def byDebits(cls):
        return [t for t in cls.instances if t.amount < 0]

    @classmethod
    def byCredits(cls):
        return [t for t in cls.instances if t.amount > 0]
    @classmethod
    def init_data_from_cursor(cls, start_date, end_date):
        cursor = mongoDbAPI.pull_transactions(start_date,end_date)
        for transaction in cursor:
            new_transaction = cls(transaction.date,transaction.amount,transaction.description)
            print(new_transaction)
Transactions.init_data_from_cursor(datetime(2026,8,5),datetime(2026,8,10))