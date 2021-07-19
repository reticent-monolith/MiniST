from models.Transaction import Transaction


class Storage:
    def __init__(self):
        # A list of transactions
        # TODO empty this list when refund works
        self.transactions = [Transaction({'transactionstartedtimestamp': '2021-06-24 14:35:54', 'parenttransactionreference': '57-9-1038877', 'interface': 'JWT-JWT-JWT', 'livestatus': '0', 'issuer': 'SecureTrading Test Issuer1', 'dccenabled': '0', 'settleduedate': '2021-06-24', 'errorcode': '0', 'baseamount': '1050', 'sitereference': 'test_benjonesthesecond84082', 'tid': '27882788', 'securityresponsepostcode': '0', 'settledtimestamp': '2021-06-25 00:25:02', 'status': 'Y', 'transactionreference': '57-9-1038878', 'threedversion': '2.1.0', 'paymenttypedescription': 'VISA', 'enrolled': 'Y',
        'merchantname': 'Ben Jones Two', 'accounttypedescription': 'ECOM', 'cavv': 'MTIzNDU2Nzg5MDEyMzQ1Njc4OTA=', 'fraudrating': '0', 'updatereason': 'settle', 'acquirerresponsecode': '00', 'eci': '05', 'requesttypedescription': 'AUTH', 'expirydate': '01/2023', 'securityresponsesecuritycode': '2', 'currencyiso3a': 'GBP', 'splitfinalnumber': '1', 'authcode': 'TEST88', 'settlebaseamount': '1050', 'errormessage': 'Ok', 'issuercountryiso2a': 'US', 'merchantcountryiso2a': 'GB', 'maskedpan': '411111######1111', 'securityresponseaddress': '0', 'operatorname': 'ben_jsapi', 'settlestatus': '100'})]

    def get(self):
        return self.transactions

    def set(self, transactions):
        self.transactions = transactions

    def add(self, transaction):
        self.transactions.append(transaction)

    def remove(self, transaction): # TODO check if this actually works without python moaning about the list changing size
        for t in self.transactions:
            if t.ref == transaction.ref:
                del t
                break

    def clear(self):
        self.transactions = []
