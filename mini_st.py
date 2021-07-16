#!/usr/bin/python
from models.Database import Database
from lib.webservices import WsConnection 
import PySimpleGUI as sg   
from threading import Thread
import lib.windows as windows
import lib.helpers as h
from models.Transaction import Transaction


###########
### GUI ###
###########

class MiniST():
    """
    Main GUI.
    """
    def __init__(self, db):
        # Flags for secondary window states
        self.windows = {
            "transaction query":    False,
            "refund":               False,
            "daily stats":          False,
            "transaction Update":   False,
            "auth":                 False,
            "account check":        False
        }

        # Create the main menu window
        self.menu = windows.menu()

        # Attach the database
        self.db = db

        # Start the GUI loop
        self.run()

    
    def run(self):
        while True:
            # Show main menu
            menu_event, menu_values = self.menu.read()

            # create connection to webservices
            self.ws = WsConnection(menu_values["WS_USER"], menu_values["WS_PASS"])
            
            # this will close the entire program
            if menu_event in ("Quit", sg.WIN_CLOSED):
                break
            # save credentials   
            # TODO make this work! No idea why it isn't... 
            elif menu_event == "Save":
                self.save_creds(menu_values["WS_USER"], menu_values["WS_PASS"])

            # handle the transactionquery window
            elif menu_event == "Transaction Query" and not self.windows["transaction query"]:
                self.windows["transaction query"] = True
                self.menu.Hide()
                self.open_transaction_query_window(menu_values)
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
                Thread(target=run_transaction_query,
                            args=(self.ws, query_filter, tq, self.db), daemon=True).start()
            elif tq_event == "-TQ_THREAD-":
                # Handle messages from the thread
                tq["_status_"].update(tq_values[tq_event])

                # If the message is 'Successful!' then print the db
                if tq_values[tq_event] == "Successful!":
                    print(self.db.transactions)
    
    def save_creds(self, user, password):
        with open(".env", "w") as file:
            file.write(f"WS_USER=\"{user}\"\n")
            file.write(f"WS_PASS=\"{password}\"\n")


#####################
### API Functions ###
#####################

# TODO move this into a different class? Controller?
def run_transaction_query(ws, query_filter, window, list_to_populate):
    """
    Run a transaction query and return a list of Transactions
    """
    window.write_event_value("-TQ_THREAD-", "Running...")

    result = ws.transaction_query(query_filter)
    if result['responses'][0]['errorcode'] != "0":
        window.write_event_value("-TQ_THREAD-", "Error!")
    else: # Successful response from API
        window.write_event_value("-TQ_THREAD-", "Successful!")
    # empty the list before adding new transactions
    if "records" in result['responses'][0].keys():
        for record in result['responses'][0]['records']:
            list_to_populate.append(Transaction(record))
    


############
### Main ###
############

if __name__=="__main__":
    db = Database()
    m = MiniST(db)

    # print(m.db)
