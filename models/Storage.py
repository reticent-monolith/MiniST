class Storage:
    def __init__(self):
        # A list of transactions
        self.transactions = []

    def add(self, transaction):
        self.transactions.append(transaction)

    def clear(self):
        self.transactions = []