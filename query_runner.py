#!/usr/bin/python
from webservices import WsConnection 
import PySimpleGUI as sg   
import threading
import windows

def main():
    tq_active = False
    while True:
        # create main menu
        menu = windows.Menu()
        menu_event, menu_values = menu.window.read()
        print(menu_values)
        # create connection to webservices
        ws = WsConnection(menu_values["WS_USER"], menu_values["WS_PASS"])

        if menu_event in ("Quit", sg.WIN_CLOSED):
            break
        elif menu_event== "TRANSACTIONQUERY" and not tq_active:
            print("tq")
            tq_active = True
            menu.window.Hide()
            while True:
                tq = windows.TransactionQuery(ws)
                tq_event, tq_values = tq.window.read()
                if tq_event == sg.WIN_CLOSED:
                    tq.window.close()
                    tq_active = False
                    menu.window.UnHide()
                    break
                if tq_event == "Run Query":
                    # Stupid python tuples and their stupid comma...
                    threading.Thread(target=tq.run_transaction_query, args=(tq_values["site_ref"],), daemon=True).start()
    menu.window.close()

if __name__=="__main__":
    main()
