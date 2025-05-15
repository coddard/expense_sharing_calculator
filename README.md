# Expense Sharing Calculator

## Description
The **Expense Sharing Calculator** is a Python script designed to fairly split shared expenses among a group of people. It allows users to input the total amount each person has paid, calculates individual balances, and generates an optimized payment plan to settle debts with transfers between as few people as possible. 

### Features
- **Group/Event Naming**: Customizable event or group name for reports.
- **Optimized Payment Plan**: Generates a minimal set of transactions to settle balances, ensuring transfers are made between as few people as possible.
- **Detailed Reporting**: Produces a summary of individual payments, balances, and transactions.
- **Export Options**: Saves reports as `.txt` (full summary) and `.csv` (transaction details).


## How to Use
Follow these steps to run and use the Expense Sharing Calculator:


### Installation
1. **Download the Script**:
   - Clone or download the repository from GitHub:
     ```bash
     git clone https://github.com/coddard/expense_sharing_calculator.git
     ```
   - Alternatively, download the script file (`expense_sharing_calculator_version103.py`) directly.

**Output**:
- The script will display a detailed report, including:
  - Individual payments and balances (who owes or is owed money).
  - Total group expenses and average per person.
  - A payment plan optimized to minimize the number of transactions (e.g., "Bob → Alice: 25.25").
- If you choose to export, files like `Weekend_Getaway_expense_report_20250516_020000.txt` and `.csv` will be created in the same directory.
### Sample Report
```plaintext
--- Expense Report: Weekend Getaway ---
Generated: 2025-05-16 02:00:00

--- Individual Balances ---
Alice               | Paid:    100.50 | is owed: 25.25
Bob                 | Paid:     75.25 | settled: 0.00
Charlie             | Paid:     50.00 | owes: 25.25

--- Group Summary ---
Total Expenses: 225.75
Average Per Person: 75.25

--- Settlement Transactions ---
Charlie → Alice: 25.25
```

### Exported Files
- **TXT File**: Contains the full report as shown above.
- **CSV File**: Lists transactions in the format:
  ```csv
  Debtor,Creditor,Amount
  Charlie,Alice,25.25
  ```
