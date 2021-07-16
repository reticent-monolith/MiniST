import PySimpleGUI as sg

sg.theme("GreenMono")

def menu():
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
    return sg.Window("MiniST", layout)



def transaction_query(ws):

    layout = [
        [sg.Text("Site Reference"), sg.Input("test_benjonesthesecond84082", key="site_ref", size=(20, 1))],

        [sg.Text("Transaction Reference"), sg.Input(key="transaction_ref", size=(20, 1))],

        [sg.Button("Run Query")]
    ]

    return sg.Window("TRANSACTIONQUERY", layout, modal=True)




