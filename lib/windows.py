import PySimpleGUI as sg
from dotenv import load_dotenv
import os

load_dotenv()
USER = os.environ.get("WS_USER")
PASS = os.environ.get("WS_PASS")

sg.theme("GreenMono")


def menu():
    """
    The layout of the main menu window
    """
    layout = [
        [sg.Text("Username"), sg.Input(
            USER, key="WS_USER", size=(20, 1))],
        [sg.Text("Password"), sg.Input(
            PASS, key="WS_PASS", size=(20, 1), password_char="*")],
        [sg.Button("Save")],
        [sg.Text("What would you like to do?")],
        [sg.Button('Transaction Query')],
        [sg.Button('Refund')],
        [sg.Button("Quit")]
    ]
    return sg.Window("MiniST", layout)


def transaction_query(user):
    """
    Layout of the transaction query window
    """
    filter_choices = ["sitereference",
                      "transactionreference (Alpha 25 char)",
                      "accounttypedescription (Alpha 20 char)",
                      "starttimestamp (YYYY-MM-DD HH:MM:SS)",
                      "endtimestamp (YYYY-MM-DD HH:MM:SS)",
                      "parenttransactionreference",
                      "paymenttypedescription",
                      "requesttypedescription",
                      "pan"
                      ]
    layout = [
        [sg.Combo(filter_choices, key="field_0"),
         sg.Input(key="value_0", size=(30, 1))],
        [sg.Combo(filter_choices, key="field_1"),
         sg.Input(key="value_1", size=(30, 1))],
        [sg.Combo(filter_choices, key="field_2"),
         sg.Input(key="value_2", size=(30, 1))],
        [sg.Combo(filter_choices, key="field_3"),
         sg.Input(key="value_3", size=(30, 1))],
        [sg.Combo(filter_choices, key="field_4"),
         sg.Input(key="value_4", size=(30, 1))],
        [sg.Combo(filter_choices, key="field_5"),
         sg.Input(key="value_5", size=(30, 1))],
        [sg.Combo(filter_choices, key="field_6"),
         sg.Input(key="value_6", size=(30, 1))],
        [sg.Combo(filter_choices, key="field_7"),
         sg.Input(key="value_7", size=(30, 1))],
        [sg.Button("Clear")],
        [sg.Output(key="_output_", size=(80, 20))],

        [sg.Button("Run Query"), sg.Button("Back")],
        [sg.Text("Idle", key="_status_", size=(50, 1))]
    ]
    return sg.Window(f"Transaction Query for {user}", layout, modal=True)


def refund(user, transactions):
    """
    Layout of the refund window
    """
    headings = ["Reference", "DateTime", "Amount"]
    for_refund = []
    trxs = transactions.get()
    for t in trxs:
        for_refund.append([t.body["transactionreference"],
                          t.body["transactionstartedtimestamp"], t.body["baseamount"]])
    # Handle an empty storage
    values = for_refund if len(for_refund) > 0 else [
        ['' for row in range(20)]for col in range(3)]
    layout = [
        [sg.Text("sitereference"), sg.Input(size=(30, 1), key="-input_site-")],
        [sg.Text("transactionreference"), sg.Input(
            size=(30, 1), key="-input_ref-")],
        [sg.Button("Add")],
        [sg.Table(
            key="-table-",
            values=values,
            headings=headings,
            def_col_width=60,
            max_col_width=60,
            # auto_size_columns=True,
            justification='center',
            # alternating_row_color='lightblue',
            num_rows=max(len(trxs), 20),
            enable_events=True,
            change_submits=True
        )],
        [sg.Button("Refund"), sg.Button("Refund All")],
        [sg.Output(size=(50, 8), key="-refund_result-")],
        [sg.Text("Idle", key="_status_", size=(50, 1))]
    ]
    return sg.Window(f"Refunds for {user}", layout, modal=True)
