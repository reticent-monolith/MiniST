import securetrading as st
from models.Transaction import Transaction


class WsConnection:
    """
    A class to connect to Trust Payments' WebServices API
    """

    # Initialise a config for the connection
    stconfig = st.Config()

    # Add auth information for the connection
    def __init__(self, user: str, password: str):
        self.stconfig.username = user
        self.stconfig.password = password

    # Create the API connection
    api = st.securetrading.Api(stconfig)

    def transaction_query(self, trx_filter: dict):
        """
        Process a TRANSACTIONQUERY with the supplied 
        filter and return the response
        """
        query = {
            "requesttypedescriptions": ["TRANSACTIONQUERY"],
            "filter": trx_filter
        }
        req = st.Request()
        req.update(query)
        return self.api.process(req)

    def refund(self, trx: Transaction, partial: str = "", updated: str = "") -> dict:
        """
        Process a refund through the api
        partial and updated will modify the type of refund if present (see TP docs)
        """
        # Don't even contact the api if settlestatus is not 100
        # if trx.body["settlestatus"] != "100":
        #     return

        refund = {
            "requesttypedescriptions": ["REFUND"],
            "sitereference": trx.site,
            "parenttransactionreference": trx.ref,
        }
        if partial != "":
            refund["baseamount"] = trx.body["baseamount"]
        if updated != "":
            refund["expirydate"] = trx.body["expirydate"]
        req = st.Request()
        req.update(refund)
        return self.api.process(req)
