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

    def transaction_query(self, trx_filter: dict[str, str]):
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

    def refund(self, to_refund: list[Transaction], partial: str = "", updated: str = ""):
        """
        Batch process refunds through the api
        to_refund is a lit of Transactions
        partial and updated will modify the type of refund if present (see TP docs)
        Returns a dict of successful transactions and failed transactions
        """
        successful = []
        failed = []
        for t in to_refund:
            refund = {
                "requesttypedescriptions": ["REFUND"],
                "sitereference": t.body["sitereference"],
                "parenttransactionreference": t.body["parenttransactionreference"],
            }
            if partial != "":
                refund["baseamount"] = t.body["baseamount"]
            if updated != "":
                refund["expirydate"] = t.body["expirydate"]
            req = st.Request()
            req.update(refund)
            result = self.api.process(req)
            if result["errorcode"] != "0" or result["settletstatus"] in ["2", "3"]:
                failed.append(result)
            else:
                successful.append(result)

        return {
            "successful": successful,
            "failed": failed
        }
