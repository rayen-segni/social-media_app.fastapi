
def add(num1: int, num2: int):
    return num1 + num2


class BankAccount:
    def __init__(self, starting_balance: int = 0) -> None:
        self.balance = starting_balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        self.amount -= amount
    
    def collect_interest(self):
        self.balance *= 1.1

