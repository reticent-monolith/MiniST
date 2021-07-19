class Storage:
    """
    To manage the in memory storage of Transactions to be operated on
    """
    def __init__(self):
        # A list of transactions
        self.transactions = []

    def get(self):
        return self.transactions

    def add(self, transaction):
        self.transactions.append(transaction)

    def remove(self, transaction): # TODO check if this actually works without python moaning about the list changing size
        for t in self.transactions:
            if t.ref == transaction.ref:
                del t
                break

    def clear(self):
        self.transactions = []
