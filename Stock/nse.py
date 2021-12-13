from nsetools import Nse


class NseData:
    nse = Nse()

    def __init__(self) -> None:
        self.nse = Nse()

    @classmethod
    def is_valid(cls,stock_code: str) -> bool:
        return cls.nse.is_valid_code(stock_code)

    @classmethod
    def get_stock_price(cls, stock_code: str) -> float:
        return cls.nse.get_quote(stock_code)['lastPrice']

    @classmethod
    def get_all_details(cls, stock_code: str) -> str:
        raw = cls.nse.get_quote(stock_code)
        output = f"*Company name*: {raw['companyName']}\n *Stock code*: {raw['symbol']}\n *isinCode*: {raw['isinCode']}\n \N{money bag} *Current price*: {raw['lastPrice']}\n \u2b06 *dayHigh*: {raw['dayHigh']}\n \u2b07 *dayLow*: {raw['dayLow']}\n \N{Chart with Upwards Trend} *52 week high*: {raw['high52']}\n \N{Chart with Downwards Trend} *52 week low*: {raw['low52']}\n "
        return output

    def get_stock_data(self, stock_code: str) -> dict:
        return self.nse.get_quote(stock_code)

    @classmethod
    def return_all_stock_codes(cls) -> list:
        return cls.nse.get_stock_codes()

# ----------------------------------------------------------------------------------------------------------------------


    @classmethod
    def search_company(cls, company_name: str) -> list:
        raw = cls.nse.get_stock_codes()
        lis = list()
        for i in raw:
            if company_name.lower() in raw[i].lower():
                lis.append(i + " - " + raw[i] + " -\t Rs. " +
                           str(NseData.get_stock_price(i)))
        return lis
