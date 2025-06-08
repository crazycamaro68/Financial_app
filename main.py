import UI
# Creates the GUI and loads classes.
if __name__ == "__main__":
    root = UI.tk.Tk()
    app = UI.FinancialManagerApp(root)
    root.mainloop()