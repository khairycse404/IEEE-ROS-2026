class BankAccount:
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited: {amount}, New Balance: {self.balance}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Withdrawn: {amount}, New Balance: {self.balance}")
        else:
            print("Insufficient balance")

acc = BankAccount()
acc.deposit(100)
acc.withdraw(200)