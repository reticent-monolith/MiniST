#!/usr/bin/python
from webservices import WsConnection 
import PySimpleGUI as sg   
import threading
import windows


def run_transaction_query(self, siteref):
    query = self.ws.transaction_query(
        {
            "sitereference": [{"value": siteref}],
            "currencyiso3a": [{"value": "GBP"}]
        }
    )
    print(query)



def gui():
    tq_active = False
    menu = windows.menu()
    while True:
        # create main menu
        menu_event, menu_values = menu.read()
        print(menu_values)
        # create connection to webservices
        ws = WsConnection(menu_values["WS_USER"], menu_values["WS_PASS"])
        if menu_event in ("Quit", sg.WIN_CLOSED):
            break
        elif menu_event== "TRANSACTIONQUERY" and not tq_active:
            tq_active = True
            menu.Hide()
            tq = windows.transaction_query(ws)
            while True:
                tq_event, tq_values = tq.read()
                print(tq_values)
                if tq_event == sg.WIN_CLOSED:
                    tq.close()
                    tq_active = False
                    menu.UnHide()
                    break
                if tq_event == "Run Query":
                    # Stupid python tuples and their stupid comma...
                    threading.Thread(target=run_transaction_query, args=(tq_values["site_ref"],), daemon=True).start()
    menu.close()


def main():
    gui()

if __name__=="__main__":
    main()
