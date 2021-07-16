class Database():
    def __init__(self):
        # A list of transactions
        self.transactions = []
    
    def append(self, transaction):
        self.transactions.append(transaction)