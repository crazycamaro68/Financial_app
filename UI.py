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

        transactions_class_creator.Transactions.load_from_dataframe(self.current_month,self.current_year)
  
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

        self.monthlyBal = ttk.Label(button_frame, text="Loading...", anchor="e", width=50)
        self.monthlyBal.grid(row=0, column=3, sticky="e", padx= 5, pady= 5)

        add_trans_button = ttk.Button(self.mathBox, text = "Add Transaction", command= self.add_transaction)
        add_trans_button.grid(row=0,column=0, padx=5, pady=5)

    def update_table_label(self):
        month_str = f"{self.current_month}/{self.current_year}"
        self.month_label.config(text=month_str)

        txns = transactions_class_creator.Transactions.instances

        try:
            start_bal = txns[0].balance - txns[0].amount
            end_bal = txns[-1].balance
            bal_text = (
                f"Starting Balance: ${start_bal:,.2f}   "
                f"Ending Balance: ${end_bal:,.2f}"
            )
        except IndexError:
            bal_text = "Starting Balance: N/A   Ending Balance: N/A"

        self.monthlyBal.config(text=bal_text)

    def create_table(self):
        if self.tree:
            self.tree.destroy()

        cols = ["Date", "Time", "Description", "Amount"]
        self.tree = ttk.Treeview(self.transList, columns=cols, show='headings')

        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.grid(row=1, column=0, sticky="nsew")

        for txn in transactions_class_creator.Transactions.instances:
            self.tree.insert("", "end", values=(txn.date, txn.time, txn.description, txn.amount))

    def change_month(self, direction):
        self.current_month += direction
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        elif self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1

        transactions_class_creator.Transactions.load_from_dataframe(self.current_month,self.current_year)
        
        self.update_table_label()
        self.create_table()
    
    def add_transaction(self):
        NAMEOFBOXES = ["Date","Time","Description","Amount"]
        popup = tk.Toplevel(self.root)
        popup.title("Add Transaction")
        
        top = ttk.Frame(popup)
        middle = ttk.Frame(popup)
        bottom = ttk.Frame(popup)
        top.grid(column=0,row=0)
        middle.grid(column=0,row=1)
        bottom.grid(column=0,row=2)
        label = ttk.Label(top, text="Add Transactions")
        label.grid(padx=20, pady=20,row=0,column=0,sticky="w")
        count = 0
        for i in NAMEOFBOXES:
            box_label = ttk.Label(middle, text=i)
            box_label.grid(column=count,row=0,padx=5,pady=5)
            box_entry = ttk.Entry(middle)
            box_entry.grid(column=count,row=1,padx=5,pady=5)
            count += 1

        ok_button = ttk.Button(bottom, text="OK", command=popup.destroy)
        ok_button.pack(pady=10)

