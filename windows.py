import PySimpleGUI as sg

sg.theme("GreenMono")

class Menu:
    layout = [
        [sg.Text("Username"), sg.Input(
            "ben_webservices", key="WS_USER", size=(20, 1))],
        [sg.Text("Password"), sg.Input(
            "BenPass123!", key="WS_PASS", size=(20, 1))],
        [sg.Text("What would you like to do?")],
        [sg.Button('TRANSACTIONQUERY')],
        [sg.Button('TRANSACTIONUPDATE')],
        [sg.Button('REFUND')],
        [sg.Button("Quit")]
    ]
    window = sg.Window("TrustPayments Merchant Query Runner", layout)



class TransactionQuery:
    def __init__(self, ws):
        self.ws = ws

    layout = [
        [sg.Text("Site Reference"), sg.Input("test_benjonesthesecond84082", key="site_ref", size=(20, 1))],

        [sg.Text("Transaction Reference"), sg.Input(key="transaction_ref", size=(20, 1))],

        [sg.Button("Run Query")]
    ]

    window = sg.Window("TRANSACTIONQUERY", layout, modal=True)
    active = False

    def run_transaction_query(self, siteref):
        query = self.ws.transaction_query(
            {
                "sitereference": [{"value": siteref}],
                "currencyiso3a": [{"value": "GBP"}]
            }
        )
        print(query)
