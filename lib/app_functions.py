"""
The functions which the gui uses to operate on the transaction 
storage and use the secure trading api.
"""

from models.Transaction import Transaction


def save_creds(user, password):
    """
    Save credentials to the .env file for ease of use
    """
    with open(".env", "w") as file:
        file.write(f"WS_USER=\"{user}\"\n")
        file.write(f"WS_PASS=\"{password}\"\n")


def run_transaction_query(ws, query_filter, window, storage):
    """
    Run a transaction query and add the records to the storage
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


def run_refund(ws, storage, window, elements):
    """
    Run multiple refunds and print the result
    """
    #TODO refactor this mess...
    storage = storage.get()
    to_refund = []
    if elements == "all":
        to_refund = storage
    else:
        for i in elements:
            to_refund.append(storage[int(i)])
    window.write_event_value("-REFUND_THREAD-", "Running...")

    refunds = []
    for t in to_refund:
        result = ws.refund(t)
        refunds.append(result)
        if result['responses'][0]['errorcode'] == "0":
            storage.remove(t)
            # Update the table with the new storage
            #TODO this needs to be a function now...
            for_refund = []
            for t in storage:
                for_refund.append([t.body["transactionreference"],
                                t.body["transactionstartedtimestamp"], t.body["baseamount"]])
            values = for_refund if len(for_refund) > 0 else [
                ['' for row in range(20)]for col in range(3)]
            window["-table-"].update(values=values)

    print(f"Refunds: {refunds}")


def add_to_storage(ws, storage, site, ref, window):
    """
    Find a transaction using transaction query and add it to the storage
    """
    transaction = ws.transaction_query({
        "sitereference": [{"value": site}],
        "transactionreference": [{"value": ref}]
    })
    try:
        storage.add(Transaction(transaction["responses"][0]["records"][0]))
    except KeyError:
        print("Invalid response from gateway")
        return
    # Update the table with the new storage
    for_refund = []
    trxs = storage.get()
    for t in trxs:
        for_refund.append([t.body["transactionreference"],
                          t.body["transactionstartedtimestamp"], t.body["baseamount"]])
    values = for_refund if len(for_refund) > 0 else [
        ['' for row in range(20)]for col in range(3)]
    window["-table-"].update(values=values)
