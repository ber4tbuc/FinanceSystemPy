import pandas as p

class Transaction:
    def __init__(self,date,amount,type,category):
        self.date=date
        self.amount=amount
        self.type=type
        self.category=category

    def displayInfo(self):
        print(f"Date:{self.date},Amount:{self.amount},Type:{self.type},Category:{self.category}")

class FinanceManager:
    def  __init__(self):
        self.transactions=[]

    def addTransaction(self,transaction):
        if not isinstance(transaction,Transaction):
            raise TypeError("Invalid input")
        self.transactions.append(transaction)
        print("Transaction added successfully.")

    def generateReport(self):
        income=sum(a.amount for a in self.transactions if a.type=="income")
        expense=sum(a.amount for a in self.transactions if a.type=="expense")
        saving=income-expense
        print("Generating report...")
        print(f"Total Income: ${float(income)}")
        print(f"Total Expenses: ${float(expense)}")
        print(f"Total Savings: ${float(saving)}")

    def filterByCategory(self, category):
        filtered = [a for a in self.transactions if a.category.lower() == category.lower()]
        if not filtered:
            print(f"No transactions found for category: {category}")
        else:
            print(f"Transactions for category '{category}':")
            for a in filtered:
                a.displayInfo()

    def saveToFile(self,filename):
        try:
            data=p.DataFrame([{"Date":a.date,"Amount":a.amount,"Type":a.type,"Category":a.category} for a in self.transactions])
            data.to_csv(filename, index=False)
            print(f"Transactions saved to {filename} successfully.")
        except Exception as e:
            print(f"Error saving to file: {e}")

    def loadFromFile(self, filename):
        try:
            df = p.read_csv(filename)
            for _, row in df.iterrows():
                transaction = Transaction(row['Date'], float(row['Amount']), row['Type'], row['Category'])
                self.transactions.append(transaction)
            print(f"Transactions loaded from {filename} successfully.")
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except Exception as e:
            print(f"Error loading from file: {e}")

    def getTopExpenses(self, n):
        expenses = [t for t in self.transactions if t.type == "expense"]
        top_expenses = sorted(expenses, key=lambda t: t.amount, reverse=True)[:n]
        print(f"Top {n} expenses:")
        for t in top_expenses:
            t.display_info()

    def getCategorySummary(self):
        summary = {}
        for t in self.transactions:
            if t.category not in summary:
                summary[t.category] = {"income": 0, "expense": 0}
            summary[t.category][t.type] += t.amount

        print("Category Summary:")
        for category, data in summary.items():
            print(f"Category: {category}, Income: ${float(data['income'])}, Expenses: ${float(data['expense'])}")


def main():
    manager = FinanceManager()

    while True:
        print("\nWelcome to the Personal Finance Management System.")
        print("1. Add Transaction")
        print("2. Generate Report")
        print("3. Filter by Category")
        print("4. Save to File")
        print("5. Load from File")
        print("6. Get Top Expenses")
        print("7. Get Category Summary")
        print("8. Exit")

        choose= input("Select an option: ")

        if choose == "1":
            try:
                date = input("Enter date (YYYY-MM-DD): ")
                amount = float(input("Enter amount: "))
                type= input("Enter type (income/expense): ").lower()
                if type not in ["income", "expense"]:
                    raise ValueError("Invalid transaction type.")
                category = input("Enter category: ")
                transaction = Transaction(date, amount, type, category)
                manager.addTransaction(transaction)
            except Exception as e:
                print(f"Error: {e}")

        elif choose == "2":
            manager.generateReport()

        elif choose == "3":
            category = input("Enter category to filter: ")
            manager.filterByCategory(category)

        elif choose == "4":
            filename = input("Enter filename to save to: ")
            manager.saveToFile(filename)

        elif choose== "5":
            filename = input("Enter filename to load from: ")
            manager.loadFromFile(filename)

        elif choose == "6":
            try:
                n = int(input("Enter the number of top expenses to display: "))
                manager.getTopExpenses(n)
            except ValueError:
                print("Invalid number.")

        elif choose == "7":
            manager.getCategorySummary()

        elif choose == "8":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
