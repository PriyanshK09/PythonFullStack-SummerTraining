from collections import defaultdict

class MetroCard:
    def __init__(self, id, balance):
        self.__id = id
        self.__src = None
        self.__balance = balance

    @property
    def id(self):
        return self.__id

    @property
    def balance(self):
        return self.__balance

    @property
    def src(self):
        return self.__src

    def add_balance(self, amount):
        self.__balance += amount

    def update_src(self, src):
        self.__src = src

class Station:
    def __init__(self, name):
        self.__name = name
        self.__total_amount = 0
        self.__discount = 0
        self.__passenger_history = defaultdict(int)

    @property
    def name(self):
        return self.__name

    @property
    def total_amount(self):
        return self.__total_amount

    @property
    def discount(self):
        return self.__discount

    @property
    def passenger_history(self):
        return self.__passenger_history

    def add_amount(self, x):
        self.__total_amount += x

    def add_discount(self, x):
        self.__discount += x

    def add_passenger(self, type):
        self.__passenger_history[type] += 1