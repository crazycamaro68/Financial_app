import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import re
import transactions_class_creator
import mongoDbAPI

class FinancialManagerApp:
    def __init__(self,root):
        self.root = root
        self.root.title("Financial Manager")

        now = datetime.now()
        self.current_month = now.month
        self.current_year = now.year

        transactions_class_creator.Transactions.init_data_from_cursor(self.current_month, self.current_year)
  
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

        add_trans_button = ttk.Button(self.mathBox, text = "Add Transaction", command= self.add_transaction)
        add_trans_button.grid(row=0,column=0, padx=5, pady=5)

        del_trans_button = ttk.Button(self.mathBox, text = "Delete Transaction", command= self.del_transaction)
        del_trans_button.grid(row=1,column=0, padx=5, pady=5)
    
    def update_table_label(self):
        month_str = f"{self.current_month}/{self.current_year}"
        self.month_label.config(text=month_str)

    def create_table(self):
        if self.tree:
            self.tree.destroy()

        cols = ["Date","Description","Amount"]
        self.tree = ttk.Treeview(self.transList, columns=cols, show='headings')

        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.grid(row=1, column=0, sticky="nsew")

        for txn in transactions_class_creator.Transactions.instances:
            self.tree.insert("", "end", values=(txn.date, txn.description, txn.amount))

    def change_month(self, direction):
        self.current_month += direction
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        elif self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1

        transactions_class_creator.Transactions.init_data_from_cursor(self.current_month,self.current_year)
        
        self.update_table_label()
        self.create_table()
    
    def add_transaction(self):
        NAMEOFBOXES = ["Description","Amount"]
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

        #Validates the Amount is a Float
        def validate_decimal_number(new_value):
            return re.match(r'^(\d+)?(\.\d*)?$', new_value) is not None
        valid_number = (self.root.register(validate_decimal_number), '%P')

        # Adds the Calender widget to allow users to select a date easily
        ttk.Label(middle, text="Date").grid(column=0,row=0,padx=5,pady=5)
        cal = DateEntry(middle, selectmode = 'day')
        cal.grid(column=0,row=1,padx=5,pady=5)

        # Generates the Descripton and Amount text boxes
        for count, name in enumerate(NAMEOFBOXES):
            ttk.Label(middle, text=name).grid(column=count+1,row=0,padx=5,pady=5)


            if name == "Amount":
                entry = ttk.Entry(middle, validate="key", validatecommand=valid_number)
            else:
                entry = ttk.Entry(middle)
            
            entry.grid(column=count+1, row=1, padx=5, pady=5)
            list_of_boxes.append(entry)
      
        #Gets data from User, formats it, creates new class objects, updates GUI.
        def on_submit():
            date_input = cal.get_date()
            desc_input = list_of_boxes[0].get()
            amount_input = list_of_boxes[1].get()

            formated_date = datetime(date_input.year,date_input.month,date_input.day)

            amount_input = float(amount_input) + .00

            new_trans = transactions_class_creator.Transactions(formated_date,desc_input,amount_input)
            mongoDbAPI.insert_transaction(new_trans)
            transactions_class_creator.Transactions.init_data_from_cursor(self.current_month, self.current_year)

            self.update_table_label()
            self.create_table()
            popup.destroy()

        ttk.Button(bottom, text="OK", command=on_submit).pack(pady=10)
    # Grabs the current highlighted transaction in the treeview and stores the values of it, searches mongodb for the entry, and then removes it from mongodb and then recreates the list
    def del_transaction(self):
        popup = tk.Toplevel(self.root)
        popup.title("Add Transaction")
        
        top = ttk.Frame(popup)
        middle = ttk.Frame(popup)
        bottom = ttk.Frame(popup)
        top.grid(column=0,row=0)
        middle.grid(column=0,row=1)
        bottom.grid(column=0,row=2)
        ttk.Label(top, text="Are you sure you want to delete?").grid(padx=20, pady=20,row=0,column=0,sticky="w")


        selected_items = self.tree.selection()
        if selected_items:
            to_be_removed = self.tree.item(selected_items,"values")
            # 

        ttk.Label(middle, text=to_be_removed).grid(padx=20, pady=20,row=0,column=0,sticky="w")
        def check_yes_no(value):
            if value == 1:
                print("I DELETED THE THINGY")
                mongoDbAPI.remove_transaction([datetime.strptime(to_be_removed[0], "%Y-%m-%d %H:%M:%S"),*to_be_removed[1:]])
                for item in selected_items:
                    self.tree.delete(item)
                popup.destroy()
            else:
                popup.destroy()
        ttk.Button(bottom, text="No", command=lambda: check_yes_no(0)).pack(pady=10)
        ttk.Button(bottom, text="Yes", command=lambda: check_yes_no(1)).pack(pady=10)