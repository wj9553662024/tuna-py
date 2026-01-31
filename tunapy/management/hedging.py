""" Parameters for hedging
"""

class TokenParameter:
    def __init__(self, conf: dict) -> None:
        self.api_key = conf['API KEY']     # the API key for Maker Account
        self.api_secret = conf['Secret']   # the API secret for Maker Account
        self.passphrase = conf['Passphrase'] # the passphrase for Maker Account

        self.maker_symbol = conf['Maker Symbol']     # the mirroring symbol
        self.hedge_symbol = conf['Hedge Symbol']     # the hedge symbol
        self.price_decimals = int(conf['Hedger Price Decimals'])      # price decimals of hedger symbol
        self.qty_decimals = int(conf['Hedger Qty Decimals'])          # quantity decimals of hedger symbol

        self.min_qty_per_order = float(conf['Min Qty'])             # minimum quantity of each order
        self.min_amt_per_order = float(conf['Min Amt'])             # minimum amount of each order
        self.slippage = max(float(conf['Slippage']), 1.0)           # slippage for hedging
