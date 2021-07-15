#!/usr/bin/python
from work import WsConnection 
from dotenv import load_dotenv
import os

# load dotenv to get variables from .dotenv
load_dotenv()

# constants
USER = os.environ.get("WS_USER")
PASSWORD = os.environ.get("WS_PASS")
SITEREF = "test_benjonesthesecond84082"

# create connection to webservices
ws = WsConnection(USER, PASSWORD)

# filter for the transaction query
trxFilter = {
    "sitereference": [{"value":SITEREF}],
    "currencyiso3a": [{"value":"GBP"}],
}

# create transaction query and store response
res = ws.transaction_query(trxFilter)

print(res)
# display response
for response in res['responses']:
    for record in response['records']:
        print(record['baseamount'])