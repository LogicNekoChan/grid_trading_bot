from binance.client import Client
from binance.enums import *
import time

class BinanceFuturesClient:
    def __init__(self, api_key, api_secret, symbol, leverage=10, isolated=True):
        self.client = Client(api_key, api_secret)
        self.symbol = symbol
        self.leverage = leverage
        self.isolated = isolated
        self.set_leverage()

    def set_leverage(self):
        self.client.futures_change_leverage(symbol=self.symbol, leverage=self.leverage)
        if self.isolated:
            self.client.futures_change_margin_type(symbol=self.symbol, marginType='ISOLATED')

    def get_klines(self, interval='1d', limit=200):
        return self.client.futures_klines(symbol=self.symbol, interval=interval, limit=limit)

    def get_account_balance(self):
        balance = self.client.futures_account_balance()
        # 返回USDT余额
        for item in balance:
            if item['asset'] == 'USDT':
                return float(item['balance'])
        return 0.0

    def place_order(self, side, quantity, price=None, order_type='LIMIT', reduce_only=False):
        params = dict(
            symbol=self.symbol,
            side=side,
            type=order_type,
            quantity=quantity,
            reduceOnly=reduce_only,
            timeInForce=TIME_IN_FORCE_GTC
        )
        if price:
            params['price'] = price
        try:
            order = self.client.futures_create_order(**params)
            return order
        except Exception as e:
            print(f"下单失败: {e}")
            return None

    def cancel_order(self, orderId):
        try:
            self.client.futures_cancel_order(symbol=self.symbol, orderId=orderId)
            return True
        except Exception as e:
            print(f"撤单失败: {e}")
            return False

    # 其他API接口如获取持仓、委托单等，待补充
