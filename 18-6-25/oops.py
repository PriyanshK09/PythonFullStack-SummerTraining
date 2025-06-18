# Functional Class Definition
# This class represents a bank account with methods to deposit and withdraw money.
class BankAccount:
    def __init__(self, amount, holder):
        self.amount = amount
        self.holder = holder
        
    def deposit(self, x):
        self.amount += x
        return self.amount
    
    def withdraw(self, x):
        self.amount -= x
        return self.amount
    
# Private and Protected Variables
class BankAccountPrivate:
    def __init__(self, amount, holder):
        self.__amount = amount  # Private variable
        self._holder = holder    # Protected variable
        
    def deposit(self, x):
        self.__amount += x
        return self.__amount
    
    def withdraw(self, x):
        self.__amount -= x
        return self.__amount
    
# SUPER Contructor Private Class
class BankAccountSuper:
    def __init__(self, amount, holder):
        self.__amount = amount  # Private variable
        self._holder = holder    # Protected variable
        
    def deposit(self, x):
        self.__amount += x
        return self.__amount
    
    def withdraw(self, x):
        self.__amount -= x
        return self.__amount
    
    def get_balance(self):
        return self.__amount  # Accessing private variable through a method
    
# Duplicate Functions (Overloading 
class BankAccountOverload:
    def __init__(self, amount, holder):
        self.amount = amount
        self.holder = holder
        
    def deposit(self, x):
        self.amount += x
        return self.amount
    
    def deposit(self, x, y=0):  # Overloaded method with default parameter
        self.amount += (x + y)
        return self.amount
    
    def withdraw(self, x):
        self.amount -= x
        return self.amount
    
    def withdraw(self, x, y=0):  # Overloaded method with default parameter
        self.amount -= (x + y)
        return self.amount
    
# Inheritance Class
class BankAccountInheritance(BankAccount):
    def __init__(self, amount, holder, account_type):
        super().__init__(amount, holder)  # Call to the parent class constructor
        self.account_type = account_type
    def display_info(self):
        return f"Holder: {self.holder}, Amount: {self.amount}, Type: {self.account_type}"
    
# Polymorphism Class
class BankAccountPolymorphism:
    def __init__(self, amount, holder):
        self.amount = amount
        self.holder = holder
        
    def deposit(self, x):
        self.amount += x
        return self.amount
    
    def withdraw(self, x):
        self.amount -= x
        return self.amount
    
    def display_balance(self):
        return f"Holder: {self.holder}, Balance: {self.amount}"
    
# Polymorphism Example
def perform_transaction(account, amount, transaction_type):
    if transaction_type == 'deposit':
        return account.deposit(amount)
    elif transaction_type == 'withdraw':
        return account.withdraw(amount)
    else:
        return "Invalid transaction type"
    
# Example usage
account1 = BankAccountPolymorphism(1000, "Alice")
account2 = BankAccountPolymorphism(2000, "Bob")

print(perform_transaction(account1, 500, 'deposit'))   # 1500
print(perform_transaction(account1, 200, 'withdraw'))  # 1300
print(perform_transaction(account2, 300, 'deposit'))   # 2300
print(perform_transaction(account2, 100, 'withdraw'))  # 2200