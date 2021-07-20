class Transaction:
    """
    A model of a transaction for requests to and responses from the API
    Takes a dict recieved from the API
    """

    def __init__(self, data: dict):
        # Build dictionary of fields and values
        self.body = data
        try:
            self.site = data["sitereference"]
            self.ref = data["transactionreference"]
        except KeyError:
            print("This isn't a valid transaction")

