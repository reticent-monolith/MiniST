#!/usr/bin/python
from webservices import WsConnection 
import PySimpleGUI as sg   
from threading import Thread
import windows



###########
### GUI ###
###########

def gui():
    """
    Main GUI thread. DO NOT RUN PYSIMPLEGUI OUTSIDE OF THIS THREAD
    """
    tq_active = False
    menu = windows.menu()
    while True:
        # create main menu
        menu_event, menu_values = menu.read()
        print(menu_values)
        # create connection to webservices
        ws = WsConnection(menu_values["WS_USER"], menu_values["WS_PASS"])
        
        # this will close the entire program
        if menu_event in ("Quit", sg.WIN_CLOSED):
            break

        # handle the transactionquery window
        elif menu_event== "TRANSACTIONQUERY" and not tq_active:
            tq_active = True
            menu.Hide()
            tq = windows.transaction_query(ws)
            while True:
                tq_event, tq_values = tq.read()
                if tq_event == sg.WIN_CLOSED:
                    tq.close()
                    tq_active = False
                    menu.UnHide()
                    break
                if tq_event == "Run Query":
                    tq.FindElement('_output_').Update('')
                    query_filter = map_values_to_filter(tq_values)
                    # Stupid python tuples and their stupid comma...
                    query = Thread(target=run_transaction_query, args=(ws, query_filter), daemon=True)
                    query.start()
    menu.close()



#####################
### API Functions ###
#####################

def run_transaction_query(ws, query_filter):
    """
    Run a transaction query
    """
    result = ws.transaction_query(query_filter)
    print(result)


########################
### Helper Functions ###
########################

def map_values_to_filter(in_values):
    """
    @param values: dict of field_n to choice and value_n to input
    """
    query_filter = dict()
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
            query_filter[pair[0]] = [pair[1]]
            fields.add(pair[0])
        else:
            query_filter[pair[0]].append(pair[1])
    return query_filter


############
### Main ###
############


def main():
    gui()

if __name__=="__main__":
    main()
