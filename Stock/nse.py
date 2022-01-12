from nsetools import Nse


class NseData:
    nse = Nse()

    def __init__(self) -> None:
        self.nse = Nse()

    @classmethod
    def is_valid(cls, stock_code: str) -> bool:
        return cls.nse.is_valid_code(stock_code)

    @classmethod
    def get_stock_price(cls, stock_code: str) -> float:
        return cls.nse.get_quote(stock_code)['lastPrice']

    @classmethod
    def get_all_details(cls, stock_code: str) -> str:
        ''' Get the complete details of the stock based on scrip code on NSE '''
        if NseData.is_valid(stock_code):
            raw = cls.nse.get_quote(stock_code)
            output = f"*Company name*: {raw['companyName']}\n *Stock code*: {raw['symbol']}\n *isinCode*: {raw['isinCode']}\n \N{money bag} *Current price*: {raw['lastPrice']}\n \u2b06 *dayHigh*: {raw['dayHigh']}\n \u2b07 *dayLow*: {raw['dayLow']}\n \N{Chart with Upwards Trend} *52 week high*: {raw['high52']}\n \N{Chart with Downwards Trend} *52 week low*: {raw['low52']}\n "
        else:
            output = f"Invalid stock code: {stock_code}"
        return output

    def chooseStockName(self, company_name_search: str) -> str:
        ''' Search the company name on NSE and return the scrip code '''
        return self.nse.get_code_by_name(company_name_search)

    def get_stock_data(self, stock_code: str) -> dict:
        return self.nse.get_quote(stock_code)

    @classmethod
    def return_all_stock_codes(cls) -> list:
        return cls.nse.get_stock_codes()

# ----------------------------------------------------------------------------------------------------------------------

    @classmethod
    def search_company(cls, company_name: str) -> list:
        ''' Search for a company name on NSE using company name'''
        raw = cls.nse.get_stock_codes()
        lis = list()
        for i in raw:
            if company_name.lower() in raw[i].lower():
                lis.append(raw[i])
        return lis

    @classmethod
    def get_details_by_name(cls, company_name: str) -> str:
        ''' Get the complete details of the stock based on company name on NSE '''
        raw = cls.nse.get_stock_codes()
        for i in raw:
            if company_name.lower() in str(raw[i]).lower():
                # print(str(raw[i]).lower() + " - " + i)
                return cls.get_all_details(i)
        return "No such company"
