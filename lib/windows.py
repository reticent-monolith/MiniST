import PySimpleGUI as sg
from dotenv import load_dotenv
import os

load_dotenv()
USER = os.environ.get("WS_USER")
PASS = os.environ.get("WS_PASS")

sg.theme("GreenMono")


def menu():
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
        [sg.Combo(filter_choices, key="field_0"), sg.Input(key="value_0", size=(30, 1))],
        [sg.Combo(filter_choices, key="field_1"), sg.Input(key="value_1", size=(30, 1))],
        [sg.Combo(filter_choices, key="field_2"), sg.Input(key="value_2", size=(30, 1))],
        [sg.Combo(filter_choices, key="field_3"), sg.Input(key="value_3", size=(30, 1))],
        [sg.Combo(filter_choices, key="field_4"), sg.Input(key="value_4", size=(30, 1))],
        [sg.Combo(filter_choices, key="field_5"), sg.Input(key="value_5", size=(30, 1))],
        [sg.Combo(filter_choices, key="field_6"), sg.Input(key="value_6", size=(30, 1))],
        [sg.Combo(filter_choices, key="field_7"), sg.Input(key="value_7", size=(30, 1))],
        [sg.Button("Clear")],
        [sg.Output(key="_output_", size=(80, 20))],

        [sg.Button("Run Query"), sg.Button("Back")],
        [sg.Text("Idle", key="_status_", size=(50, 1))]
    ]

    return sg.Window(f"Transaction Query for {user}", layout, modal=True)


def refund(user, transactions):
    transactions = [{'transactionstartedtimestamp': '2021-06-24 14:35:54', 'parenttransactionreference': '57-9-1038877', 'interface': 'JWT-JWT-JWT', 'livestatus': '0', 'issuer': 'SecureTrading Test Issuer1', 'dccenabled': '0', 'settleduedate': '2021-06-24', 'errorcode': '0', 'baseamount': '1050', 'sitereference': 'test_benjonesthesecond84082', 'tid': '27882788', 'securityresponsepostcode': '0', 'settledtimestamp': '2021-06-25 00:25:02', 'status': 'Y', 'transactionreference': '57-9-1038878', 'threedversion': '2.1.0', 'paymenttypedescription': 'VISA', 'enrolled': 'Y', 'merchantname': 'Ben Jones Two', 'accounttypedescription': 'ECOM', 'cavv': 'MTIzNDU2Nzg5MDEyMzQ1Njc4OTA=', 'fraudrating': '0', 'updatereason': 'settle', 'acquirerresponsecode': '00', 'eci': '05', 'requesttypedescription': 'AUTH', 'expirydate': '01/2023', 'securityresponsesecuritycode': '2', 'currencyiso3a': 'GBP', 'splitfinalnumber': '1', 'authcode': 'TEST88', 'settlebaseamount': '1050', 'errormessage': 'Ok', 'issuercountryiso2a': 'US', 'merchantcountryiso2a': 'GB', 'maskedpan': '411111######1111', 'securityresponseaddress': '0', 'operatorname': 'ben_jsapi', 'settlestatus': '100'}]
    headings = ["Reference", "DateTime", "Amount"]
    for_refund = []
    for t in transactions:
        for_refund.append([t["transactionreference"], t["transactionstartedtimestamp"], t["baseamount"]])

    layout = [
        [sg.Table(
            values=for_refund,
            headings=headings,
            max_col_width=25,
            auto_size_columns=True,
            justification='right',
            # alternating_row_color='lightblue',
            num_rows=min(len(transactions), 20)
        )],
        [sg.Button("Refund")]
    ]

    return sg.Window(f"Refunds for {user}", layout, modal=True)
