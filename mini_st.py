#!/usr/bin/python
from lib.Controller import Controller
from models.Storage import Storage
from lib.Webservices import WsConnection
import PySimpleGUI as sg
from threading import Thread
import lib.windows as windows
import lib.helpers as h
from models.Transaction import Transaction


###########
### GUI ###
###########

def save_creds(user, password):
    with open(".env", "w") as file:
        file.write(f"WS_USER=\"{user}\"\n")
        file.write(f"WS_PASS=\"{password}\"\n")


class MiniST:
    """
    Main GUI.
    """

    def __init__(self, storage, controller):
        # Flags for secondary window states
        self.ws = None
        self.windows = {
            "transaction query": False,
            "refund": False,
            "daily stats": False,
            "transaction Update": False,
            "auth": False,
            "account check": False
        }

        # Create the main menu window
        self.menu = windows.menu()

        # Attach the database
        self.storage = storage

        # Start the GUI loop
        self.run()

    def run(self):
        while True:
            # Show main menu
            menu_event, menu_values = self.menu.read()
            self.ws = WsConnection(menu_values["WS_USER"], menu_values["WS_PASS"])
            # create connection to webservices

            # this will close the entire program
            if menu_event in ("Quit", sg.WIN_CLOSED):
                break
            # save credentials   
            # TODO make this work! No idea why it isn't... 
            elif menu_event == "Save":
                save_creds(menu_values["WS_USER"], menu_values["WS_PASS"])

            # handle the transactionquery window
            elif menu_event == "Transaction Query" and not self.windows["transaction query"]:
                self.windows["transaction query"] = True
                self.menu.Hide()
                self.open_transaction_query_window(menu_values)
                self.menu.UnHide()

            # handle the refund window
            elif menu_event == "Refund" and not self.windows["refund"]:
                self.windows["refund"] = True
                self.menu.Hide()
                self.open_refund_window(menu_values)
                self.menu.UnHide()

        # Close the window                    
        self.menu.close()

    def open_transaction_query_window(self, menu_values):
        tq = windows.transaction_query(menu_values["WS_USER"])
        while True:
            tq_event, tq_values = tq.read()
            if tq_event in (sg.WIN_CLOSED, "Back"):
                tq.close()
                self.windows["transaction query"] = False
                break
            elif tq_event == "Clear":
                # clear the inputs
                for el in list(tq.element_list()):
                    if isinstance(el, sg.Input) or isinstance(el, sg.Combo):
                        el.update("")
            elif tq_event == "Run Query":
                # clear the output
                tq.FindElement('_output_').Update('')
                # contruct the filter for the query
                query_filter = h.map_values_to_dict(tq_values)
                # Run the query in a new thread
                Thread(target=controller.run_transaction_query,
                       args=(self.ws, query_filter, tq, self.storage), daemon=True).start()
            elif tq_event == "-TQ_THREAD-":
                # Handle messages from the thread
                tq["_status_"].update(tq_values[tq_event])
                # If the message is 'Successful!' then print the db
                if tq_values[tq_event] == "Successful!":
                    # TODO improve display here
                    print(self.storage.transactions[0].body)

    def open_refund_window(self, menu_values):
        win = windows.refund(menu_values["WS_USER"], self.storage.transactions)
        while True:
            e, v = win.read()
            print(v)
            if e in (sg.WIN_CLOSED, "Back"):
                win.close()
                self.windows["refund"] = False
                break
            elif e == "Refund":
                Thread(target=controller.run_refund,
                       args=(self.ws, self.storage.transactions, win), daemon=True).start()
            elif e == "-TQ_THREAD-":
                # Handle messages from the thread
                win["_status_"].update(v[e])
                # If the message is 'Successful!' then print the db
                if v[e] == "Successful!":
                    # TODO improve display here
                    print(self.storage.transactions[0].body)


############
### Main ###
############

if __name__ == "__main__":
    storage = Storage()
    controller = Controller()
    m = MiniST(storage, controller)

    # print(m.db)
