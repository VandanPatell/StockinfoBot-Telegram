import json
from bsedata.bse import BSE


class bse:

    bseObj = BSE()

    def __init__(self) -> None:
        """
        This is bse class that will fetch and return various realtime information from BSE (Bombay Stock Exchange).
        Author : Vandan Patel
        """
        # bseObj.updateScripCodes()
        # print("bse Class created")

    @classmethod
    def search_companies_by_name(cls, companyName) -> str:
        raw = cls.bseObj.getScripCodes()
        list = []
        for i in raw:
            if companyName.lower() in raw[i].lower():
                list.append(raw[i])
        return list

    @classmethod
    def get_details_by_name(cls, companyName) -> str:
        raw = cls.bseObj.getScripCodes()
        for i in raw:
            if companyName.lower() == raw[i].lower():
                output = f"*Company name*: {raw[i]}\n *Stock code*: {i}\n *scripCode*: {raw['securityID']}\n \N{money bag} *Current price*: {cls.bseObj.getQuote(i)['currentValue']}\n \u2b06 *dayHigh*: {cls.bseObj.getQuote(i)['dayHigh']}\n \u2b07 *dayLow*: {cls.bseObj.getQuote(i)['dayLow']}\n \N{Chart with Upwards Trend} *52 week high*: {cls.bseObj.getQuote(i)['52weekHigh']}\n \N{Chart with Downwards Trend} *52 week low*: {cls.bseObj.getQuote(i)['52weekLow']}\n "
            else:
                continue
        return output

    @classmethod
    def get_all_details_by_scripCode(cls, ScripCode) -> str:
        if ScripCode in cls.bseObj.getScripCodes():
            raw = cls.bseObj.getQuote(ScripCode)
            output = f"*Company name*: {raw['companyName']}\n *Stock code*: {raw['securityID']}\n *scripCode*: {raw['scripCode']}\n \N{money bag} *Current price*: {raw['currentValue']}\n \u2b06 *dayHigh*: {raw['dayHigh']}\n \u2b07 *dayLow*: {raw['dayLow']}\n \N{Chart with Upwards Trend} *52 week high*: {raw['52weekHigh']}\n \N{Chart with Downwards Trend} *52 week low*: {raw['52weekLow']}\n "
            return output
        else:
            return "Invalid Scrip Code"
