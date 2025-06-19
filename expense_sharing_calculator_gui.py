import tkinter as tk
from tkinter import messagebox
import json

class Person:
    def __init__(self, name):
        self.name = name
        self.paid = 0.0
        self.owed = 0.0
        self.balance = 0.0
    
    def set_total_paid(self, amount_str):
        try:
            amount = float(amount_str)
        except ValueError:
            raise ValueError("Invalid amount: must be a number")
        if amount < 0:
            raise ValueError("Total paid cannot be negative")
        self.paid = amount

def calculate_summary(people):
    total = sum(p.paid for p in people)
    avg = total / len(people) if len(people) > 0 else 0
    return total, avg

def optimize_transactions(people):
    # Calculate balances
    total, avg = calculate_summary(people)
    for p in people:
        p.balance = p.paid - avg
    
    # Optimize settlement
    debtors = [p for p in people if p.balance < 0]
    creditors = [p for p in people if p.balance > 0]
    transactions = []
    
    debtors.sort(key=lambda x: x.balance)
    creditors.sort(key=lambda x: x.balance, reverse=True)
    
    d_idx = 0
    c_idx = 0
    
    while d_idx < len(debtors) and c_idx < len(creditors):
        debtor = debtors[d_idx]
        creditor = creditors[c_idx]
        
        amount = min(-debtor.balance, creditor.balance)
        transactions.append((debtor.name, creditor.name, round(amount, 2)))
        
        debtor.balance += amount
        creditor.balance -= amount
        
        if abs(debtor.balance) < 0.01:
            d_idx += 1
        if abs(creditor.balance) < 0.01:
            c_idx += 1
            
    return transactions

def generate_report(event_name, people, total, avg, transactions, currency_symbol):
    report = f"Expense Report for {event_name}\n"
    report += "=" * 50 + "\n"
    report += f"Total amount spent: {currency_symbol}{total:.2f}\n"
    report += f"Average per person: {currency_symbol}{avg:.2f}\n\n"
    
    report += "Individual Balances:\n"
    for p in people:
        report += f"{p.name}: Paid {currency_symbol}{p.paid:.2f}, Should Pay {currency_symbol}{avg:.2f}, "
        if p.balance >= 0:
            report += f"Gets Back {currency_symbol}{p.balance:.2f}\n"
        else:
            report += f"Owes {currency_symbol}{-p.balance:.2f}\n"
    
    report += "\nSettlement Transactions:\n"
    if not transactions:
        report += "No transactions needed. Everyone is settled!\n"
    else:
        for t in transactions:
            report += f"{t[0]} pays {t[1]} {currency_symbol}{t[2]:.2f}\n"
    
    return report

def export_reports(report, event_name, transactions):
    # Export text report
    with open(f"{event_name}_expense_report.txt", "w") as f:
        f.write(report)
    
    # Export JSON transactions
    json_data = [{"from": t[0], "to": t[1], "amount": t[2]} for t in transactions]
    with open(f"{event_name}_transactions.json", "w") as f:
        json.dump(json_data, f, indent=2)

# Create the main window
root = tk.Tk()
root.title("Expense Sharing Calculator")

# Description label
description_label = tk.Label(root, text="Expense Sharing Calculator\nEnter the event name, number of people, and their payments to calculate who owes whom.")
description_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Event name
event_label = tk.Label(root, text="Event/Group Name:")
event_label.grid(row=1, column=0, sticky="e")
event_entry = tk.Entry(root)
event_entry.grid(row=1, column=1, sticky="w")

# Currency symbol
currency_label = tk.Label(root, text="Currency Symbol:")
currency_label.grid(row=2, column=0, sticky="e")
currency_entry = tk.Entry(root, width=5)
currency_entry.grid(row=2, column=1, sticky="w")
currency_entry.insert(0, "$")  # Default currency symbol

# Number of people
num_people_label = tk.Label(root, text="Number of People:")
num_people_label.grid(row=3, column=0, sticky="e")
num_people_entry = tk.Entry(root)
num_people_entry.grid(row=3, column=1, sticky="w")

# Generate button
generate_button = tk.Button(root, text="Generate Input Fields", command=lambda: generate_fields())
generate_button.grid(row=4, column=0, columnspan=2, pady=10)

# People frame
people_frame = tk.Frame(root)
people_frame.grid(row=5, column=0, columnspan=2)

# Calculate button
calculate_button = tk.Button(root, text="Calculate", command=lambda: calculate())
calculate_button.grid(row=6, column=0, columnspan=2, pady=10)

# Report text
report_text = tk.Text(root, height=15, width=80)
report_text.grid(row=7, column=0, columnspan=2, sticky="nsew")
report_text.config(state=tk.DISABLED)

# Export button
export_button = tk.Button(root, text="Export Reports", command=lambda: export_reports_gui())
export_button.grid(row=8, column=0, columnspan=2, pady=10)

# Lists to hold entry widgets
name_entries = []
amount_entries = []

# Global variables for report
current_event_name = ""
current_report = ""
current_transactions = []

def generate_fields():
    try:
        num_people = int(num_people_entry.get())
        if num_people <= 0:
            raise ValueError("Number of people must be positive")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    # Clear existing widgets in people_frame
    for widget in people_frame.winfo_children():
        widget.destroy()

    name_entries.clear()
    amount_entries.clear()

    for i in range(num_people):
        name_label = tk.Label(people_frame, text=f"Person {i+1} Name:")
        name_label.grid(row=i, column=0, sticky="e")
        name_entry = tk.Entry(people_frame)
        name_entry.grid(row=i, column=1, sticky="w")
        amount_label = tk.Label(people_frame, text="Total Paid:")
        amount_label.grid(row=i, column=2, sticky="e")
        amount_entry = tk.Entry(people_frame)
        amount_entry.grid(row=i, column=3, sticky="w")
        name_entries.append(name_entry)
        amount_entries.append(amount_entry)

def calculate():
    global current_event_name, current_report, current_transactions
    event_name = event_entry.get().strip()
    if not event_name:
        messagebox.showerror("Error", "Event name cannot be empty")
        return
    
    currency_symbol = currency_entry.get().strip()
    if not currency_symbol:
        currency_symbol = "$"  # Default to dollar sign if empty

    people = []
    used_names = set()
    for name_entry, amount_entry in zip(name_entries, amount_entries):
        name = name_entry.get().strip()
        amount = amount_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Name cannot be empty")
            return
        if name in used_names:
            messagebox.showerror("Error", "Duplicate name")
            return
        used_names.add(name)
        person = Person(name)
        try:
            person.set_total_paid(amount)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        people.append(person)

    if not people:
        messagebox.showerror("Error", "No participants entered")
        return

    total, avg = calculate_summary(people)
    transactions = optimize_transactions(people)
    report = generate_report(event_name, people, total, avg, transactions, currency_symbol)
    report_text.config(state=tk.NORMAL)
    report_text.delete(1.0, tk.END)
    report_text.insert(tk.END, report)
    report_text.config(state=tk.DISABLED)
    current_event_name = event_name
    current_report = report
    current_transactions = transactions

def export_reports_gui():
    if not current_report:
        messagebox.showerror("Error", "No report to export")
        return
    export_reports(current_report, current_event_name, current_transactions)
    messagebox.showinfo("Success", "Reports exported successfully")

# Configure grid weights for resizing
root.grid_rowconfigure(7, weight=1)  # Adjusted for the new row layout
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Start the main loop
root.mainloop()