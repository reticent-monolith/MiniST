from models.Transaction import Transaction


class Controller:
    def __init__(self):
        pass

    def run_transaction_query(self, ws, query_filter, window, storage):
        """
        Run a transaction query and return a list of Transactions
        """
        # Communicate with main thread that a query is starting
        window.write_event_value("-TQ_THREAD-", "Running...")
        # clear previous transactions from storage
        storage.clear()
        result = ws.transaction_query(query_filter)
        if result['responses'][0]['errorcode'] != "0":
            window.write_event_value("-TQ_THREAD-", "Error!")
        else:  # Successful response from API
            window.write_event_value("-TQ_THREAD-", "Successful!")
        # empty the list before adding new transactions
        if "records" in result['responses'][0].keys():
            for record in result['responses'][0]['records']:
                storage.add(Transaction(record))

    def run_refund(self, ws, transaction_list, window):
        """
        Run multiple refunds and return a dictionary of successful and failed refunds
        """
        window.write_event_value("-REFUND_THREAD-", "Running...")

