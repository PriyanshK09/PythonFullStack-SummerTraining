def __add__(self, other):
    if isinstance(other, BankAccount):
        return BankAccount(self.amount + other.amount, self.holder)
    return NotImplemented

def __sub__(self, other):
    if isinstance(other, BankAccount):
        return BankAccount(self.amount - other.amount, self.holder)
    return NotImplemented

def __eq__(self, other):
    if isinstance(other, BankAccount):
        return self.amount == other.amount and self.holder == other.holder
    return NotImplemented

class BankAccount:
    def __init__(self, amount, holder):
        self.amount = amount
        self.holder = holder

    def __str__(self):
        return f"BankAccount(holder={self.holder}, amount={self.amount})"

    def __repr__(self):
        return f"BankAccount({self.amount}, '{self.holder}')"
    
    # Operator overloading methods
    __add__ = __add__
    __sub__ = __sub__
    __eq__ = __eq__
    
    # Making a wrong operator overloading for demonstration like for ge <=
    def __ge__(self, other):
        if isinstance(other, BankAccount):
            return self.amount <= other.amount
        return NotImplemented
    
# Usage example
def main():
    account1 = BankAccount(1000, "Alice")
    account2 = BankAccount(500, "Bob")
    
    print(account1)  # Output: BankAccount(holder=Alice, amount=1000)
    print(account2)  # Output: BankAccount(holder=Bob, amount=500)
    
    account3 = account1 + account2
    print(account3)  # Output: BankAccount(holder=Alice, amount=1500)
    
    account4 = account1 - account2
    print(account4)  # Output: BankAccount(holder=Alice, amount=500)
    
    print(account1 == account2)  # Output: False
    print(account1 == BankAccount(1000, "Alice"))  # Output: True
    
    print(account1 >= account2) # Output: False (due to wrong operator overloading)
    
if __name__ == "__main__":
    main()
# This code defines a BankAccount class with operator overloading for addition, subtraction, and equality checks.