#!/usr/bin/python
from lib.app_functions import *
from models.Storage import Storage
from lib.Webservices import WsConnection
import PySimpleGUI as sg
from threading import Thread
import lib.windows as windows
import lib.helpers as h


class MiniST:
    """
    Main GUI.
    """

    def __init__(self, storage):
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
        """
        The main loop to run the program. Other loops are nested within 
        this one when a new window is opened.
        """
        while True:
            # Show main menu
            menu_event, menu_values = self.menu.read()
            # create connection to webservices
            self.ws = WsConnection(
                menu_values["WS_USER"], menu_values["WS_PASS"])
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
                self.windows["transaction query"] = False
                self.menu.UnHide()
            # handle the refund window
            elif menu_event == "Refund" and not self.windows["refund"]:
                self.windows["refund"] = True
                self.menu.Hide()
                print(self.storage.get())
                self.open_refund_window(menu_values)
                self.windows["refund"] = False
                self.menu.UnHide()

        # Close the window
        self.menu.close()

    def open_transaction_query_window(self, menu_values):
        """
        Opens and manages the transaction query window
        """
        window = windows.transaction_query(menu_values["WS_USER"])
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Back"):
                window.close()
                break
            elif event == "Clear":
                # clear the inputs
                for el in list(window.element_list()):
                    if isinstance(el, sg.Input) or isinstance(el, sg.Combo):
                        el.update("")
            elif event == "Run Query":
                # clear the output
                window.FindElement('_output_').Update('')
                # contruct the filter for the query
                query_filter = h.map_values_to_dict(values)
                # Run the query in a new thread
                Thread(target=run_transaction_query,
                       args=(self.ws, query_filter, window, self.storage), daemon=True).start()
            elif event == "-TQ_THREAD-":
                # Handle messages from the thread
                window["_status_"].update(values[event])
                # If the message is 'Successful!' then print the db
                if values[event] == "Successful!":
                    # TODO improve display here
                    print(self.storage.transactions[0].body)

    def open_refund_window(self, menu_values):
        """
        Opens and manages the refund window
        """
        window = windows.refund(menu_values["WS_USER"], self.storage)
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Back"):
                window.close()
                break
            if event == "Add":
                if values["-input_ref-"] != "" and values["-input_site-"] != "":
                    Thread(target=add_to_storage,
                        args=(self.ws, self.storage,
                                values["-input_site-"], values["-input_ref-"], window),
                        daemon=True).start()
                else:
                    print("No data entered")
            elif event == "Refund":
                if len(values["-table-"]) > 0:
                    Thread(target=run_refund,
                        args=(self.ws, self.storage, window, values["-table-"]),
                        daemon=True).start()
                else:
                    print("Select at least one transaction")
            elif event == "Refund All":
                if len(values["-table-"]) > 0:
                    Thread(target=run_refund,
                        args=(self.ws, self.storage, window, "all"),
                        daemon=True).start()


############
### Main ###
############

if __name__ == "__main__":
    storage = Storage()
    m = MiniST(storage)
