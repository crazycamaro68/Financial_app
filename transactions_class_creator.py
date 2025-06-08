import pandas as pd
from datetime import datetime

class Transactions:
    instances = []
    df = pd.read_excel("master_transaction.xlsx", sheet_name=1, parse_dates=["Date"])
    current_date = datetime.now()

    def __init__(self, date, time, description, amount, balance):
        self.date = date
        self.time = time
        self.description = description
        self.amount = amount
        self.balance = balance

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

    @classmethod
    def load_from_dataframe(cls, month=None, year=None):
        if month is None:
            month = cls.current_date.month
        if year is None:
            year = cls.current_date.year

        cls.instances.clear()

        filtered_df = cls.df[(cls.df["Date"].dt.month == month) & (cls.df["Date"].dt.year == year)]

        for _, row in filtered_df.iterrows():
            date = row["Date"].date()
            transaction = cls(date, row["Time"], row["Description"], row["Amount"], row["Balance"])
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
