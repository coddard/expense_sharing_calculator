import csv
import datetime
from decimal import Decimal, getcontext, InvalidOperation

getcontext().prec = 28  # Increased precision to handle larger numbers

# ---- ASCII Art ve Tanımlamalar ----
def print_ascii_art():
    print("""
░░░░░░▄▄▄▄▀▀▀▀▀▀▀▀▄▄▄▄▄▄▄
░░░░░█░░░░░░░░░░░░░░░░░░▀▀▄
░░░░█░░░░░░░░░░░░░░░░░░░░░░█
░░░█░░░░░░▄██▀▄▄░░░░░▄▄▄░░░░█
░▄▀░▄▄▄░░█▀▀▀▀▄▄█░░░██▄▄█░░░░█
█░░█░▄░▀▄▄▄▀░░░░░░░░█░░░░░░░░░█
█░░█░█▀▄▄░░░░░█▀░░░░▀▄░░▄▀▀▀▄░█
░█░▀▄░█▄░█▀▄▄░▀░▀▀░▄▄▀░░░░█░░█
░░█░░░▀▄▀█▄▄░█▀▀▀▄▄▄▄▀▀█▀██░█
░░░█░░░░██░░▀█▄▄▄█▄▄█▄▄██▄░░█
░░░░█░░░░▀▀▄░█░░░█░█▀█▀█▀██░█
░░░░░▀▄░░░░░▀▀▄▄▄█▄█▄█▄█▄▀░░█
░░░░░░░▀▄▄░░░░░░░░░░░░░░░░░░░█
░░▐▌░█░░░░▀▀▄▄░░░░░░░░░░░░░░░█
░░░█▐▌░░░░░░█░▀▄▄▄▄▄░░░░░░░░█
░░███░░░░░▄▄█░▄▄░██▄▄▄▄▄▄▄▄▀
░▐████░░▄▀█▀█▄▄▄▄▄█▀▄▀▄
░░█░░▌░█░░░▀▄░█▀█░▄▀░░░█
░░█░░▌░█░░█░░█░░░█░░█░░█
░░█░░▀▀░░██░░█░░░█░░█░░█
░░░▀▀▄▄▀▀░█░░░▀▄▀▀▀▀█░░█
░░░░░░░░░░█░░░░▄░░▄██▄▄▀
░░░░░░░░░░█░░░░▄░░████
░░░░░░░░░░█▄░░▄▄▄░░▄█
░░░░░░░░░░░█▀▀░▄░▀▀█
░░░░░░░░░░░█░░░█░░░█
░░░░░░░░░░░█░░░▐░░░█
░░░░░░░░░░░█░░░▐░░░█
░░░░░░░░░░░█░░░▐░░░█
░░░░░░░░░░░█░░░▐░░░█
░░░░░░░░░░░█▄▄▄▐▄▄▄█
░░░░░░░▄▄▄▄▀▄▄▀█▀▄▄▀▄▄▄▄
░░░░░▄▀▄░▄░▄░░░█░░░▄░▄░▄▀▄
░░░░░█▄▄▄▄▄▄▄▄▄▀▄▄▄▄▄▄▄▄▄█

------------------------------------------------------------------------------
Expense Sharing Calculator

Description:
This Python program helps fairly split shared expenses among a group.
Enter the total amount paid by each person. The program calculates
who owes whom and provides a summary report and payment plan.
It also allows exporting the report.

Features:
- Input total amount paid per person (supports 50, 50.75, 50,75)
- Group/Event naming
- Calculates individual totals, group total, and average
- Generates an optimized payment plan (who pays whom)
- Provides a summary report
- Exports report to .txt and .csv
------------------------------------------------------------------------------
    """)

# ---- Person Class ----
class Person:
    """
    Represents a person participating in expense sharing.
    """
    def __init__(self, name):
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        self.name = name.strip()
        self.total_paid = Decimal('0.00')
        self.balance = Decimal('0.00')

    def set_total_paid(self, amount):
        """Handles all valid number formats and normalizes to two decimal places."""
        try:
            # Convert to string and standardize decimal separator
            cleaned = str(amount).replace(",", ".")
            
            # Check if amount is a valid number
            try:
                float(cleaned)  # Test if it can be converted to float
            except ValueError:
                raise ValueError("Not a valid number format")
            
            # Split into integer and decimal parts
            if '.' in cleaned:
                integer_part, decimal_part = cleaned.split('.', 1)
                decimal_part = decimal_part.ljust(2, '0')[:2]  # Ensure two decimal places
            else:
                integer_part = cleaned
                decimal_part = "00"
            
            # Rebuild the normalized amount string
            normalized = f"{integer_part}.{decimal_part}"
            
            # Convert to Decimal and validate
            try:
                amount_dec = Decimal(normalized)
                if amount_dec < Decimal('0'):
                    raise ValueError("Amount cannot be negative.")
                
                self.total_paid = amount_dec.quantize(Decimal('0.01'))
                print(f"   Recorded payment for {self.name}: {self.total_paid:.2f}")
            except InvalidOperation:
                raise ValueError(f"Could not convert '{normalized}' to a valid decimal number")
                
        except Exception as e:
            raise ValueError(f"Invalid amount: {str(e)}")
            
    def calculate_balance(self, average):
        """Calculates balance against group average."""
        self.balance = self.total_paid - average

# ---- Helper Functions ----
def validate_input(prompt, validation_func, error_msg):
    """Generic input validator with detailed error handling."""
    while True:
        user_input = input(prompt).strip()
        try:
            result = validation_func(user_input)
            return result
        except Exception as e:
            print(f"{error_msg}: {str(e)}")
            continue

def sanitize_filename(name):
    """Removes special characters from filenames."""
    return "".join([c if c.isalnum() else "_" for c in name])

# ---- Core Logic ----
def get_group_info():
    """Gets validated group/event name."""
    return validate_input(
        "Enter event/group name: ",
        lambda x: x if x else ValueError("Name cannot be empty."),
        "Invalid name"
    )

def get_people_and_their_payments():
    """Collects payment data with robust validation."""
    num_people = validate_input(
        "Number of people: ",
        lambda x: int(x) if x.isdigit() and int(x) > 0 else ValueError("Must be > 0."),
        "Invalid number"
    )

    people = []
    used_names = set()

    for i in range(num_people):
        name = validate_input(
            f"Person {i+1} name: ",
            lambda x: x.strip() if x.strip() and x.strip() not in used_names else ValueError("Invalid/duplicate name."),
            "Name error"
        )
        used_names.add(name)
        person = Person(name)

        while True:
            try:
                amount = input(f"  Total paid by {name} (e.g., 50, 50.75, or 50,75): ").strip()
                # Try simple conversion to test if valid number
                cleaned = amount.replace(",", ".")
                float(cleaned)  # This will raise ValueError if not a valid number
                
                person.set_total_paid(amount)
                break  # Break the loop if set_total_paid succeeds
            except Exception as e:
                print(f"Amount error: {str(e)}")
                
        people.append(person)
    
    return people

def calculate_summary(people):
    """Calculates total and average with Decimal precision."""
    total = sum(p.total_paid for p in people)
    avg = (total / len(people)).quantize(Decimal('0.01')) if people else Decimal('0.00')
    for p in people:
        p.calculate_balance(avg)
    return total.quantize(Decimal('0.01')), avg

def optimize_transactions(people):
    """Generates optimized debt settlement transactions."""
    debtors = sorted(
        [{"name": p.name, "owe": -p.balance} for p in people if p.balance < Decimal('0')],
        key=lambda x: x["owe"], 
        reverse=True
    )
    creditors = sorted(
        [{"name": p.name, "owed": p.balance} for p in people if p.balance > Decimal('0')],
        key=lambda x: x["owed"], 
        reverse=True
    )

    transactions = []
    d_idx, c_idx = 0, 0

    while d_idx < len(debtors) and c_idx < len(creditors):
        debtor = debtors[d_idx]
        creditor = creditors[c_idx]
        amount = min(debtor["owe"], creditor["owed"])

        if amount > Decimal('0.01'):  # Only add meaningful transactions
            transactions.append((
                debtor["name"], 
                creditor["name"], 
                amount.quantize(Decimal('0.01'))
            ))

        debtor["owe"] -= amount
        creditor["owed"] -= amount

        if debtor["owe"] <= Decimal('0.01'):
            d_idx += 1
        if creditor["owed"] <= Decimal('0.01'):
            c_idx += 1

    return transactions

# ---- Reporting ----
def generate_report(event_name, people, total, avg, transactions):
    """Generates a detailed expense report."""
    report = [
        f"\n--- Expense Report: {event_name} ---",
        f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "\n--- Individual Balances ---"
    ]
    
    for p in people:
        status = ("owes" if p.balance < Decimal('0') else 
                 "is owed" if p.balance > Decimal('0') else 
                 "settled")
        report.append(
            f"{p.name.ljust(20)} | Paid: {str(p.total_paid).rjust(10)} | {status}: {abs(p.balance):.2f}"
        )
    
    report.extend([
        "\n--- Group Summary ---",
        f"Total Expenses: {total:.2f}",
        f"Average Per Person: {avg:.2f}",
        "\n--- Settlement Transactions ---"
    ])
    
    if transactions:
        for debtor, creditor, amount in transactions:
            report.append(f"{debtor} → {creditor}: {amount:.2f}")
    else:
        report.append("All balances are settled. No transactions needed.")
    
    return "\n".join(report)

def export_reports(report_content, event_name, transactions):
    """Exports reports to TXT and CSV formats."""
    safe_name = sanitize_filename(event_name)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"{safe_name}_expense_report_{timestamp}"

    # TXT Export
    try:
        with open(f"{base_filename}.txt", "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"\nTXT report saved: {base_filename}.txt")
    except IOError as e:
        print(f"Error saving TXT: {str(e)}")

    # CSV Export
    try:
        with open(f"{base_filename}.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Debtor", "Creditor", "Amount"])
            for t in transactions:
                writer.writerow([t[0], t[1], f"{t[2]:.2f}"])
        print(f"CSV report saved: {base_filename}.csv")
    except Exception as e:
        print(f"Error saving CSV: {str(e)}")

# ---- Main Function ----
def main():
    print_ascii_art()
    
    event_name = get_group_info()
    people = get_people_and_their_payments()
    
    if not people:
        print("\nError: No participants entered. Exiting.")
        return
    
    total_expenses, average = calculate_summary(people)
    transactions = optimize_transactions(people)
    
    report = generate_report(event_name, people, total_expenses, average, transactions)
    print(report)
    
    if input("\nExport reports? (y/n): ").lower().startswith("y"):
        export_reports(report, event_name, transactions)
    
    print("\nProcess completed successfully.")

if __name__ == "__main__":
    main()