#!/usr/bin/python
from lib.app_functions import *
from models.Storage import Storage
from lib.Webservices import WsConnection
import PySimpleGUI as PSG
from threading import Thread
import lib.windows as windows
import lib.helpers as h
import pprint


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
            if menu_event in ("Quit", PSG.WIN_CLOSED):
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
                print(self.storage.get())
                self.menu.UnHide()
            # handle the refund window
            elif menu_event == "Refund" and not self.windows["refund"]:
                self.windows["refund"] = True
                self.menu.Hide()
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
            if event in (PSG.WIN_CLOSED, "Back"):
                window.close()
                break
            elif event == "Clear":
                # clear the inputs
                for el in list(window.element_list()):
                    if isinstance(el, PSG.Input) or isinstance(el, PSG.Combo):
                        el.update("")
            elif event == "Run Query":
                # clear the output
                window.FindElement('_output_').Update('')
                # construct the filter for the query
                query_filter = h.map_values_to_dict(values)
                # Run the query in a new thread
                Thread(target=run_transaction_query,
                       args=(self.ws, query_filter, window, self.storage), daemon=True).start()
            elif event == "-TQ_THREAD-":
                # Handle messages from the thread
                window["_status_"].update(values[event])
                # If the message is 'Successful!' then print the db
                if values[event] == "Successful!":
                    count = 0
                    for t in self.storage.get():
                        count += 1
                        print(f"### Transaction {count} ###\n")
                        pprint.pprint(t.body)
                        print()
                    print(f"Found {count} transactions")

    def open_refund_window(self, menu_values):
        """
        Opens and manages the refund window
        """
        window = windows.refund(menu_values["WS_USER"], self.storage)
        while True:
            event, values = window.read()
            # CLose the window
            if event in (PSG.WIN_CLOSED, "Back"):
                window.close()
                break
            if event == "Add":
                if values["-input_ref-"] != "" and values["-input_site-"] != "":
                    Thread(target=add_to_storage,
                           args=(self.ws, self.storage,
                                 values["-input_site-"], values["-input_ref-"], window),
                           daemon=True).start()
                    window["-input_ref-"].update("")
                else:
                    print("ERROR: No data entered")
            elif event == "Refund":
                if len(values["-table-"]) > 0:
                    Thread(target=run_refund,
                           args=(self.ws, self.storage,
                                 window, values["-table-"]),
                           daemon=True).start()
                else:
                    print("ERROR: Select at least one transaction")
            elif event == "Refund All":
                if len(values["-table-"]) > 0:
                    Thread(target=run_refund,
                           args=(self.ws, self.storage, window, "all"),
                           daemon=True).start()
            elif event == "-REFUND_THREAD-":
                if values["-REFUND_THREAD-"] == "Done":
                    print("\nRefunds processed. If any of the selected transactions are left in the table, "
                          "they failed. Check to ensure a refund is possible on them")
            elif event == "View":
                selected = values["-table-"]
                if len(selected) > 0:
                    PSG.popup(pprint.pformat(self.storage.get()[int(selected[0])].body))


############
### Main ###
############

if __name__ == "__main__":
    storage = Storage()
    m = MiniST(storage)
