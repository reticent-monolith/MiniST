import PySimpleGUI as sg
from dotenv import load_dotenv
import os

from lib.app_functions import get_refund_table_values

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
        # [sg.Button("Save")],
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
        [sg.Text("Select a field on the left (or enter your own) and enter the value.")],
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
    headings = [x.ljust(15) for x in ["Reference", "DateTime     ", "Amount"]]
    trxs = transactions.get()
    layout = [
        [sg.Text("Enter a site reference and transaction reference to add transactions here.")],
        [sg.Text("Alternatively, transactions that can be refunded will be imported here")],
        [sg.Text("from a transaction query.")],
        [sg.Text("sitereference"), sg.Input(size=(30, 1), key="-input_site-")],
        [sg.Text("transactionreference"), sg.Input(
            size=(30, 1), key="-input_ref-")],
        [sg.Button("Add")],
        [sg.Text("Select a transaction and right-click > View to view more details.")],
        [sg.Table(
            key="-table-",
            values=get_refund_table_values(trxs),
            headings=headings,
            justification='center',
            num_rows=20,
            enable_events=True,
            change_submits=True,
            right_click_menu=['&Right', ['View']]
        )],
        [sg.Button("Refund"), sg.Button("Refund All")],
        [sg.Output(size=(57, 5), key="-refund_result-")],
        [sg.Text("Idle", key="_status_", size=(50, 1))]
    ]
    return sg.Window(f"Refunds for {user}", layout, modal=True)
