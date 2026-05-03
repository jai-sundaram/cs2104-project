import csv
from datetime import datetime

user_expenses = []
#reading the expenses from the file and storing the expenses in a list 
def load():

    with open("../data/expenses.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["amount"] = float(row["amount"])
            user_expenses.append(row)
##saves the expenses to a file
def save():
    with open("expenses.csv", "w", newline="") as file:
        fieldnames = ["name", "amount", "category", "date"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(user_expenses)
#validates that the amount the user enters is possible (positive amount), and that is an actual number 
def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("Amount must be greater than 0.")
            else:
                return amount
        except ValueError:
            print("Please enter a valid number.")
##ensures that the date format is valid, enforcing the Year-Month-Date format 
def get_valid_date():
    while (True):
        date = input("Enter date (YYYY-MM-DD): ")
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            print("Invalid date format.")
##allows the user to add an expense 
def add():
    name = input("Enter expense name: ")
    amount = get_valid_amount()
    category = input("Enter category: ")
    date = get_valid_date()
    expense = {
        "name": name,
        "amount": amount,
        "category": category,
        "date": date
    }
    user_expenses.append(expense)
    save()
    print("Expense added successfully.\n")
#allows the user to view their expenses 
def view():
    if (not user_expenses):
        print("No expenses recorded.\n")
        return
    print("\nAll Expenses:")
    print("-" * 50)
    i = 1
    for exp in user_expenses:
        print(f"{i}. {exp['date']} | {exp['name']} | ${exp['amount']:.2f} | {exp['category']}")
        i +=1
    print("-" * 50)
    print()
#allows the user to delete an expense 
def delete():
    view()
    if (not user_expenses):
        return
    try:
        choice = int(input("Enter the number of the expense to delete: "))

        if(choice >= 1 and choice <= len(user_expenses)):
            removed = user_expenses.pop(choice - 1)
            save()
            print(f"Deleted: {removed['name']}\n")
        else:
            print("Invalid expense number.\n")

    except ValueError:
        print("Please enter a valid number.\n")
#shows the total spending
def total_spending():
    total = 0 
    for exp in user_expenses:
        total += exp["amount"]
    print(f"\nTotal spending: ${total:.2f}\n")
#organizes the spending into categories 
def c_summary():
    if (not user_expenses):
        print("No expenses recorded.\n")
        return
    summary = {}
    for exp in user_expenses:
        category = exp["category"]
        summary[category] = summary.get(category, 0) + exp["amount"]
    print("\nSpending by Category:")
    print("-" * 35)
    for category, total in summary.items():
        print(f"{category}: ${total:.2f}")
    print("-" * 35)
    print()
#helps the user view their expenses for a particular month/year 
def m_summary():
    month = input("Enter month to search (YYYY-MM): ")
    monthly_expenses = []
    for exp in user_expenses:
        if (exp["date"].startswith(month)):
            monthly_expenses.append(exp)
    if not monthly_expenses:
        print("No expenses found for that month.\n")
        return
    total = 0
    for exp in monthly_expenses:
        total += exp["amount"]
    print(f"\nMonthly Summary for {month}")
    print("-" * 40)
    for exp in monthly_expenses:
        print(f"{exp['date']} | {exp['name']} | {exp['category']} | ${exp['amount']:.2f}")
    print("-" * 40)
    print(f"Total for {month}: ${total:.2f}\n")
#Tells the user how they are doing compared to the budget they set 
def budget():
    budget = get_valid_amount()
    total = 0 
    for exp in user_expenses:
        total += exp["amount"]

    print(f"\nMonthly Budget: ${budget:.2f}")
    print(f"Current Spending: ${total:.2f}")

    if (total > budget):
        print(f"You are over budget by ${total - budget:.2f}.\n")
    else:
        print(f"You are under budget by ${budget - total:.2f}. Good job!\n")
#exports their expenses as a text file 
def export():
    report_name = "expense_report.txt"
    total = 0
    for exp in user_expenses:
        total += exp["amount"]

    with open(f"../docs/{report_name}", "w") as file:
        file.write("Expense Tracker Report\n")
        file.write("======================\n\n")

        file.write("All Expenses:\n")
        for exp in user_expenses:
            file.write(f"{exp['date']} | {exp['name']} | ${exp['amount']:.2f} | {exp['category']}\n")

        file.write(f"\nTotal Spending: ${total:.2f}\n")

    print(f"Report exported to {report_name}.\n")
#the menu/main way for the user to interact with the program 
def menu():
    load()
    while (True):
        print("==== Personal Budget and Expense Tracker ====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Total Spending")
        print("5. Category Summary")
        print("6. Monthly Summary")
        print("7. Budget Check")
        print("8. Export Report")
        print("9. Exit")
        choice = input("Choose an option: ")
        if (choice == "1"):
            add()
        elif (choice == "2"):
            view()
        elif (choice == "3"):
            delete()
        elif (choice == "4"):
            total_spending()
        elif (choice == "5"):
            c_summary()
        elif (choice == "6"):
            m_summary()
        elif (choice == "7"):
            budget()
        elif (choice == "8"):
            export()
        elif (choice == "9"):
            print("Goodbye. Thank you for your use of the program.")
            break
        else:
            print("Invalid option.\n")
menu()