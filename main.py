import transactions_class_creator
import pandas as pd
import UI

# Loads excel sheet and creates classes for it.
df = pd.read_excel("master_transaction.xlsx", sheet_name=1)
transactions_class_creator.Transactions.load_from_dataframe(df)

# Creates the GUI and loads classes.
if __name__ == "__main__":
    root = UI.tk.Tk()
    app = UI.FinancialManagerApp(root)
    root.mainloop()