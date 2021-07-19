"""
The functions which the gui uses to operate on the transaction 
storage and use the secure trading api.
"""

from PySimpleGUI.PySimpleGUI import Window
from models.Storage import Storage
from models.Transaction import Transaction
from lib.Webservices import WsConnection
from lib.helpers import *


def save_creds(user: str, password: str):
    """
    Save credentials to the .env file for ease of use
    """
    with open(".env", "w") as file:
        file.write(f"WS_USER=\"{user}\"\n")
        file.write(f"WS_PASS=\"{password}\"\n")


def run_transaction_query(ws: WsConnection, query_filter: dict, window: Window, storage: Storage):
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


def run_refund(ws: WsConnection, storage: Storage, window: Window, elements: list):
    """
    Run multiple refunds and print the result
    """
    storage = storage.get()
    # Prepare the selected transactions of refund
    to_refund = []
    if elements == "all":
        to_refund = storage
    else:
        for i in elements:
            to_refund.append(storage[int(i)])
    window.write_event_value("-REFUND_THREAD-", "Running...")
    # Process the refunds via the api
    refunds = []
    for t in to_refund:
        result = ws.refund(t)
        refunds.append(result)
        print(f"Refunding {t.ref}:\n {result}")
        # If the refund was successful, remove the transaction from storage
        if result['responses'][0]['errorcode'] == "0":
            storage.remove(t)
            # Update the table with the new storage
            window["-table-"].update(values=get_table_values(storage))
    window.write_event_value("-REFUND_THREAD-", "Done")
    

def add_to_storage(ws: WsConnection, storage: Storage, site: str, ref: str, window: Window):
    """
    Find a transaction using transaction query and add it to the storage
    """
    transaction = ws.transaction_query({
        "sitereference": [{"value": site.strip()}],
        "transactionreference": [{"value": ref.strip()}]
    })
    try:
        storage.add(Transaction(transaction["responses"][0]["records"][0]))
    except KeyError:
        print("Invalid response from gateway")
        return
    # Update the table with the new storage
    window["-table-"].update(values=get_table_values(storage.get()))



