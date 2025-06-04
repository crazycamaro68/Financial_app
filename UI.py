import tkinter as tk
from tkinter import ttk
from datetime import datetime
import transactions_class_creator

class FinancialManagerApp:
    def __init__(self,root):
        self.root = root
        self.root.title("Financial Manager")

        now = datetime.now()
        self.current_month = now.month
        self.current_year = now.year
  
        self.current_trans = transactions_class_creator.Transactions.byMonth(self.current_month, self.current_year)
        self.tree = None

        self.setup_layout()
        self.update_table_label()
        self.create_table()

    def setup_layout(self):
        self.transList = ttk.Frame(self.root)
        self.transList.grid(row=0, column=0, sticky="nsew")
        self.transList.columnconfigure(0, weight=1)
        self.transList.rowconfigure(1, weight=1)

        self.mathBox = ttk.Frame(self.root)
        self.mathBox.grid(row=0, column=1, sticky="nsew")

        button_frame = ttk.Frame(self.transList)
        button_frame.grid(row=0, column=0, sticky="ew", padx=5)
        button_frame.columnconfigure(0, weight=0)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=0)

        prev_button = ttk.Button(button_frame, text="Previous Month", command=lambda: self.change_month(-1))
        prev_button.grid(row=0, column=0, sticky="w")

        self.month_label = ttk.Label(button_frame, text="Loading...")
        self.month_label.grid(row=0, column=1, sticky="n", padx=10)

        next_button = ttk.Button(button_frame, text="Next Month", command=lambda: self.change_month(1))
        next_button.grid(row=0,column=2,sticky="n")

        try:
            balance_text = f"Starting Balance: {self.current_trans[0].balance}   Ending Balance: {self.current_trans[-1].balance}"
        except:
            balance_text = "Starting Balance: N/A   Ending Balance: N/A"

        self.monthlyBal = ttk.Label(button_frame, text=balance_text, anchor="e", width=45)
        self.monthlyBal.grid(row=0, column=3, sticky="e")

    def update_table_label(self):
        month_name = f"{self.current_month}/{self.current_year}"
        self.month_label.config(text=month_name)

        try:
            self.monthlyBal.config(text=f"Starting Balance: {self.current_trans[0].balance} Ending Balance: {self.current_trans[-1].balance}")
        except:
            pass

    def create_table(self):
        if self.tree:
            self.tree.destroy()

        cols = ["Date", "Time", "Description", "Amount"]
        self.tree = ttk.Treeview(self.transList, columns=cols, show='headings')

        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.grid(row=1, column=0, sticky="nsew")

        for txn in self.current_trans:
            self.tree.insert("", "end", values=(txn.date, txn.time, txn.description, txn.amount))

    def change_month(self, direction):
        self.current_month += direction
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        elif self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1

        self.current_trans = transactions_class_creator.Transactions.byMonth(self.current_month, self.current_year)
        
        self.update_table_label()
        self.create_table()

