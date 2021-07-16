class Transaction:
    """
    A model of a transaction for requests to and responses from the API
    Takes tuple pairs of field and value
    """
    def __init__(self, data):
        # Build dictionary of fields and values
        self.body = data

