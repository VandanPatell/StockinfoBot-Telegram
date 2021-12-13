import json
from bsedata.bse import BSE
# 

class bse:

    bseObj = BSE()

    def __init__(self) -> None:
        """
        This is bse class that will fetch and return various realtime information from BSE (Bombay Stock Exchange).
        Author : Vandan Patel
        """
        self.bseObj.updateScripCodes()
        print("bse Class created")

    def getcripcodes(self):
        return self.bseObj.getScripCodes()

    @classmethod
    def check_scripCode(cls, scripCode: str) -> bool:
        """
        This method will check whether the the given scrip code exists or not.

        Args:
            scripCode (int): the scrip code of the stock for eg: 5128965 

        Returns:
            bool: Will return the boolean value.
        """
        if cls.bseObj.verifyScripCode(scripCode) != None:
            return True

        return False

    @classmethod
    def get_company_name(cls, scripCode: str) -> str:

        if bse.check_scripCode(scripCode):
            return cls.bseObj.verifyScripCode(scripCode)
        else:
            return "Invalid ScripCode"

    @classmethod
    def get_scrip_code(cls, company_alias: str) -> str:
        raw = cls.bseObj.getScripCodes()
        found = False
        for i in raw:
            if company_alias.lower() in raw[i].lower():
                found = True
                return str(i)

        if not found:
            return "No Company found."

    @classmethod
    def get_stock_price(cls, scripCode: str = None, company_name: str = None) -> int:
        if scripCode == None and company_name == None:
            return None
        elif scripCode == None:
            raw = cls.bseObj.getScripCodes()
            for i in raw:
                if company_name.lower() in raw[i].lower():
                    json_obj = cls.bseObj.getQuote(i)
                    return json_obj['currentValue']
        elif company_name == None:
            a = cls.bseObj.getQuote(scripCode=scripCode)
            return a['currentValue']

    @classmethod
    def searchCompany(cls, companyName) -> str:
        raw = cls.bseObj.getScripCodes()
        companies = str()
        for i in raw:
            if companyName.lower() in raw[i].lower():
                companies = companies + "\n" + raw[i]

        return companies
