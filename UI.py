import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re
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
            formated_date = datetime.strftime(txn.date, "%m-%d-%Y")
            formated_time = datetime.strftime(datetime.strptime(txn.time,"%H:%M"),"%I:%M %p")
            self.tree.insert("", "end", values=(formated_date,formated_time , txn.description, txn.amount))

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
        list_of_boxes = []

        popup = tk.Toplevel(self.root)
        popup.title("Add Transaction")
        
        top = ttk.Frame(popup)
        middle = ttk.Frame(popup)
        bottom = ttk.Frame(popup)
        top.grid(column=0,row=0)
        middle.grid(column=0,row=1)
        bottom.grid(column=0,row=2)
        ttk.Label(top, text="Add Transactions").grid(padx=20, pady=20,row=0,column=0,sticky="w")

        #text box validators
        def validate_time(time):
            if time == "":
                return True
            return re.match(r'^[0-9:\sapmAPM]*$', time) is not None
        def validate_decimal_number(new_value):
            return re.match(r'^(\d+)?(\.\d*)?$', new_value) is not None
        
        valid_time = (self.root.register(validate_time), '%P')
        valid_number = (self.root.register(validate_decimal_number), '%P')

        for count, name in enumerate(NAMEOFBOXES):
            ttk.Label(middle, text=name).grid(column=count,row=0,padx=5,pady=5)

            if name == "Time":
                entry = ttk.Entry(middle, validate="key", validatecommand=valid_time)
            elif name == "Amount":
                entry = ttk.Entry(middle, validate="key", validatecommand=valid_number)
            else:
                entry = ttk.Entry(middle)
            
            entry.grid(column=count, row=1, padx=5, pady=5)
            list_of_boxes.append(entry)

        def parse_date_flexibly(date_str):
            formats = ["%m/%d/%y", "%m/%d/%Y", "%Y-%m-%d", "%m-%d-%Y", "%m-%d-%y"]
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            return None
        
        def parse_time_flexibly(time_str):
            formats = ["%H:%M", "%I:%M %p", "%I:%M%p"]
            for fmt in formats:
                try:
                    return datetime.strptime(time_str.strip(), fmt)
                except ValueError:
                    continue
            return None
        
        #Gets data from text boxes, formats it, creates new class objects, updates GUI.
        def on_submit():
            date_input = list_of_boxes[0].get()
            time_input = list_of_boxes[1].get()
            desc_input = list_of_boxes[2].get()
            amount_input = list_of_boxes[3].get()

            # Validate and reformat date
            date_obj = parse_date_flexibly(date_input)
            if not date_obj:
                messagebox.showerror("Invalid Date", "Enter a valid date (e.g. 12/31/25, 2025-12-31).")
                return
            formatted_date = datetime.strptime(date_obj.strftime("%Y-%m-%d"),"%Y-%m-%d")

            #Validate and reformat time
            time_input = ' '.join(time_input.strip().upper().split())
            time_obj = parse_time_flexibly(time_input)
            if not time_obj:
                messagebox.showerror("Invalid Time", "Enter time like 2:30 PM or 14:30.")
                return
            formatted_time = time_obj.strftime("%H:%M")

            amount_input = float(amount_input) + .00

            balance = None
            new_trans = transactions_class_creator.Transactions(formatted_date,formatted_time,desc_input,amount_input,balance)
            
            self.timeline_insert(new_trans)
            self.update_table_label()
            self.create_table()
            popup.destroy()

        ttk.Button(bottom, text="OK", command=on_submit).pack(pady=10)

    def recalculate_balances(self, start_index):
        instances = transactions_class_creator.Transactions.instances
        for i in range(start_index, len(instances)):
            #Checks if new transaction is at the start and cal orgianal balance before and then updates it to the new transaction.
            if i == 0:
                if len(instances) > 1 and instances[1].balance is not None:
                    inferred_start_balance = instances[1].balance - instances[1].amount
                    instances[0].balance = inferred_start_balance + instances[0].amount
            else:
                instances[i].balance = instances[i-1].balance + instances[i].amount
    
    def timeline_insert(self,new_object):
        index = 0
        instances = transactions_class_creator.Transactions.instances

        while index < len(instances):
            current_object = instances[index]
            
            if new_object.date < current_object.date:
                break
            elif new_object.date == current_object.date:
                if new_object.time <= current_object.time:
                    break
                else:
                    index += 1
            else:
                index += 1

        transactions_class_creator.Transactions.instances.insert(index,new_object)
        self.recalculate_balances(index)   