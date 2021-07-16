#!/usr/bin/python
from lib.webservices import WsConnection 
import PySimpleGUI as sg   
from threading import Thread
import lib.windows as windows



###########
### GUI ###
###########

def gui():
    """
    Main GUI thread.
    """

    # Flags for secondary window states
    tq_active = False

    # Create the main menu window
    menu = windows.menu()
    while True:
        # create main menu
        menu_event, menu_values = menu.read()

        # create connection to webservices
        ws = WsConnection(menu_values["WS_USER"], menu_values["WS_PASS"])
        
        # this will close the entire program
        if menu_event in ("Quit", sg.WIN_CLOSED):
            break
        # save credentials   
        # TODO make this work! No idea why it isn't... 
        elif menu_event == "Save":
            save_creds(menu_values["WS_USER"], menu_values["WS_PASS"])

        # handle the transactionquery window
        elif menu_event== "Transaction Query" and not tq_active:
            tq_active = True
            menu.Hide()
            tq = windows.transaction_query(menu_values["WS_USER"])
            while True:
                tq_event, tq_values = tq.read()
                if tq_event in (sg.WIN_CLOSED, "Back"):
                    tq.close()
                    tq_active = False
                    menu.UnHide()
                    break
                elif tq_event == "Clear":
                    for el in list(tq.element_list()):
                        if isinstance(el, sg.Input) or isinstance(el, sg.Combo):
                            el.update("")
                elif tq_event == "Run Query":
                    tq.FindElement('_output_').Update('')
                    query_filter = map_values_to_dict(tq_values)
                    query = Thread(target=run_transaction_query, args=(ws, query_filter, tq), daemon=True)
                    query.start()
                elif tq_event == "-TQ_THREAD-":
                    tq["_status_"].update(tq_values[tq_event])

    # Close the window                    
    menu.close()



#####################
### API Functions ###
#####################

def run_transaction_query(ws, query_filter, window):
    """
    Run a transaction query
    """
    window.write_event_value("-TQ_THREAD-", "Running...")

    result = ws.transaction_query(query_filter)
    if result['responses'][0]['errorcode'] != "0":
        window.write_event_value("-TQ_THREAD-", "Error!")
    else: # Successful response from API
        window.write_event_value("-TQ_THREAD-", "Successful!")
    count = 0
    if "records" in result['responses'][0].keys():
        for record in result['responses'][0]['records']:
            count += 1
            print(f"#### Record {count} ####")
            for k,v in record.items():
                print(f"{k}: {v}")
            print()
    
    


########################
### Helper Functions ###
########################

def map_values_to_dict(in_values):
    """
    @param values: dict of field_n to choice and value_n to input
    """
    output = dict()
    fields = ['']*8
    values = ['']*8

    for k, v in in_values.items():
        # Ignore empty fields and their related values
        if v != "":
            if "field_" in k:
                # trim field down to what api expects, as format guidance is in our string too
                fields[int(k.split("_")[1])] = v.split(" ")[0]
            if "value_" in k:
                # adjust value to dict
                values[int(k.split("_")[1])] = {"value" : v}

    # Map fields to their respective values, except if field contains input but value is blank
    fields = [f for f in fields if f != '']
    values = [v for v in values if v != '']
    zipped = list(zip(fields, values))

    # merge multiple values for same field into lists
    fields = set()
    for pair in zipped:
        if pair[0] not in fields:
            output[pair[0]] = [pair[1]]
            fields.add(pair[0])
        else:
            output[pair[0]].append(pair[1])
    return output

def save_creds(user, password):
    with open(".env", "w") as file:
        file.write(f"WS_USER=\"{user}\"\n")
        file.write(f"WS_PASS=\"{password}\"\n")

############
### Main ###
############

def main():
    gui()

if __name__=="__main__":
    main()
