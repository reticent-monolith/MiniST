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
        [sg.Combo(filter_choices, key="field_0"), sg.Input(key="value_0", size=(20, 1))],
        [sg.Combo(filter_choices, key="field_1"), sg.Input(key="value_1", size=(20, 1))],
        [sg.Combo(filter_choices, key="field_2"), sg.Input(key="value_2", size=(20, 1))],
        [sg.Combo(filter_choices, key="field_3"), sg.Input(key="value_3", size=(20, 1))],
        [sg.Combo(filter_choices, key="field_4"), sg.Input(key="value_4", size=(20, 1))],
        [sg.Combo(filter_choices, key="field_5"), sg.Input(key="value_5", size=(20, 1))],
        [sg.Combo(filter_choices, key="field_6"), sg.Input(key="value_6", size=(20, 1))],
        [sg.Combo(filter_choices, key="field_7"), sg.Input(key="value_7", size=(20, 1))],

        [sg.Output(key="_output_", size=(80,20))],

        [sg.Button("Run Query")]
    ]

    return sg.Window("TRANSACTIONQUERY", layout, modal=True)




