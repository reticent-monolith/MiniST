class Transaction:
    """
    A model of a transaction for requests to and responses from the API
    Takes tuple pairs of field and value
    """

    def __init__(self, data):
        # Build dictionary of fields and values
        self.body = data
        print(f"Creating Transaction: {data}")
        try:
            self.site = data["sitereference"]
            self.ref = data["transactionreference"]
        except KeyError:
            print("This isn't a valid transaction")

