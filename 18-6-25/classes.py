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

    def __str__(self):
        return f"Account holder: {self.holder}, Balance: {self.amount}"


class SavingsAccount(BankAccount):
    def __init__(self, amount, holder, interest_rate):
        super().__init__(amount, holder)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self.amount * self.interest_rate
        self.amount += interest
        return self.amount


class CheckingAccount(BankAccount):
    def __init__(self, amount, holder, overdraft_limit):
        super().__init__(amount, holder)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, x):
        if self.amount + self.overdraft_limit >= x:
            self.amount -= x
            return self.amount
        else:
            raise ValueError("Withdrawal exceeds overdraft limit")


class BusinessAccount(BankAccount):
    def __init__(self, amount, holder, business_name):
        super().__init__(amount, holder)
        self.business_name = business_name

    def deposit(self, x):
        if x > 0:
            return super().deposit(x)
        else:
            raise ValueError("Deposit amount must be positive")

    def withdraw(self, x):
        if x > 0:
            return super().withdraw(x)
        else:
            raise ValueError("Withdrawal amount must be positive")


class JointAccount(BankAccount):
    def __init__(self, amount, holders):
        if len(holders) < 2:
            raise ValueError("Joint account must have at least two holders")
        super().__init__(amount, holders)
        self.holders = holders

    def deposit(self, x):
        return super().deposit(x)

    def withdraw(self, x):
        return super().withdraw(x)

    def __str__(self):
        return f"Joint holders: {', '.join(self.holders)}, Balance: {self.amount}"


class FixedDepositAccount(BankAccount):
    def __init__(self, amount, holder, maturity_date):
        super().__init__(amount, holder)
        self.maturity_date = maturity_date

    def withdraw(self, x):
        raise ValueError("Cannot withdraw from a fixed deposit account before maturity")

    def add_interest(self, interest_rate):
        interest = self.amount * interest_rate
        self.amount += interest
        return self.amount

    def __str__(self):
        return f"Fixed Deposit - Holder: {self.holder}, Balance: {self.amount}, Maturity Date: {self.maturity_date}"

# Savings Account
savings = SavingsAccount(1000, "Priyansh", 0.05)
print("SavingsAccount Initial:", savings)
savings.deposit(500)
savings.add_interest()
print("After Deposit and Interest:", savings)

# Checking Account
checking = CheckingAccount(500, "Priyansh", 200)
print("\nCheckingAccount Initial:", checking)
checking.withdraw(600)
print("After Withdraw within overdraft:", checking)
try:
    checking.withdraw(200)
except ValueError as e:
    print("Overdraft Exceeded:", e)

# Business Account
business = BusinessAccount(10000, "Priyansh", "Promo Pulse")
print("\nBusinessAccount Initial:", business)
business.deposit(2000)
business.withdraw(1500)
print("After Transactions:", business)
try:
    business.deposit(-500)
except ValueError as e:
    print("Invalid Deposit:", e)

# Joint Account
joint = JointAccount(3000, ["Priyansh", "Anuj"])
print("\nJointAccount Initial:", joint)
joint.deposit(1000)
joint.withdraw(500)
print("After Transactions:", joint)

# Fixed Deposit Account
fixed = FixedDepositAccount(20000, "Priyansh", "2026-12-31")
print("\nFixedDepositAccount Initial:", fixed)
fixed.add_interest(0.07)
print("After Interest:", fixed)
try:
    fixed.withdraw(1000)
except ValueError as e:
    print("Withdrawal Attempt:", e)
