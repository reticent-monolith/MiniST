########################
### Helper Functions ###
########################

def map_values_to_dict(in_values):
    """
    @param in_values: dict of field_n to choice and value_n to input
    """
    output = dict()
    fields: list[str] = ['']*8
    values: list[str] = [''] * 8

    for k, v in in_values.items():
        # Ignore empty fields and their related values
        if v != "":
            if "field_" in k:
                # trim field down to what api expects, as format guidance is in our string too
                fields[int(k.split("_")[1])] = v.split(" ")[0]
            if "value_" in k:
                # adjust value to dict
                values[int(k.split("_")[1])] = {"value": v}

    # Map fields to their respective values, except if field contains input but value is blank
    fields = [f for f in fields if f != '']
    values = [v for v in values if v != '']
    zipped = list(zip(fields, values))

    # merge multiple values for same field into lists
    used_fields = set()
    for pair in zipped:
        if pair[0] not in used_fields:
            output[pair[0]] = [pair[1]]
            used_fields.add(pair[0])
        else:
            output[pair[0]].append(pair[1])
    return output


def get_table_values(transactions: list) -> list:
    """
    Returns a list of rows for the refund table, or an empty list if there are no
    transactions in storage
    """
    for_refund = []
    for t in transactions:
        try:
            if t.body["requesttypedescription"] == "AUTH":
                for_refund.append([t.body["transactionreference"],
                                t.body["transactionstartedtimestamp"], 
                                t.body["baseamount"],
                                t.body["settlestatus"],
                                t.body["requesttypedescription"],
                                ])
        except:
            pass #TODO What shoudl happn here?
    
    return for_refund if len(for_refund) > 0 else [
        ['' for row in range(20)]for col in range(5)]
