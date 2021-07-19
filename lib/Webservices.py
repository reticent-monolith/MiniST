import securetrading as st

from models.Transaction import Transaction


class WsConnection:
    """
    A class to connect to Trust Payments' WebServices API
    """

    # Initialise a config for the connection
    stconfig = st.Config()

    # Add auth information for the connection
    def __init__(self, user, password):
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

    def refund(self, to_refund: Transaction, partial: str = "", updated: str = "") -> dict:
        """
        Process a refund through the api
        partial and updated will modify the type of refund if present (see TP docs)
        """
        print(f"to refund: {to_refund}")
        refund = {
            "requesttypedescriptions": ["REFUND"],
            "sitereference": to_refund.site,
            "parenttransactionreference": to_refund.ref,
        }
        if partial != "":
            refund["baseamount"] = to_refund.body["baseamount"]
        if updated != "":
            refund["expirydate"] = to_refund.body["expirydate"]
        req = st.Request()
        req.update(refund)
        return self.api.process(req)
        
