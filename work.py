import securetrading as st

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
    
    
    def transaction_query(self, filter):
        """
        Process a TRANSACTIONQUERY with the supplied 
        filter and return the response
        """
        query = {
            "requesttypedescriptions": ["TRANSACTIONQUERY"],
            "filter": filter
        }
        req = st.Request()
        req.update(query)
        return self.api.process(req)

    def account_check(self):
        pass