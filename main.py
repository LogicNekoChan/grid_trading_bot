# main.py
import time
import pandas as pd

from config import *
from binance_futures import BinanceFuturesClient
from trend_detector import detect_trend
from fibo_calculator import calc_fibo_levels, find_high_low
from grid_executor import GridExecutor
from risk_manager import RiskManager

def main():
    client = BinanceFuturesClient(BINANCE_API_KEY, BINANCE_SECRET_KEY)
    risk_manager = RiskManager(LONG_PARAMS['max_position'], SHORT_PARAMS['max_position'])

    while True:
        # 获取K线数据
        raw_klines = client.get_klines(SYMBOL, '1d', limit=200)
        df = pd.DataFrame(raw_klines, columns=['open_time','open','high','low','close','volume','close_time',
                                               'quote_asset_volume','number_of_trades','taker_buy_base','taker_buy_quote','ignore'])
        df['close'] = df['close'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)

        # 趋势判断
        trend = detect_trend(df)

        # 计算斐波那契区间
        high, low = find_high_low(df['high'].tolist())
        if trend == 'LONG':
            fibo_levels = calc_fibo_levels(low, high, LONG_PARAMS['fibo_ratios'])
            max_pos = LONG_PARAMS['max_position']
        elif trend == 'SHORT':
            fibo_levels = calc_fibo_levels(low, high, SHORT_PARAMS['fibo_ratios'])
            max_pos = SHORT_PARAMS['max_position']
        else:
            time.sleep(60)
            continue

        # 资金和仓位管理
        balance_info = client.client.futures_account_balance()
        usdt_balance = float([x['balance'] for x in balance_info if x['asset']=='USDT'][0])
        current_position = client.get_position(SYMBOL)
        current_pos_amt = float(current_position['positionAmt']) if current_position else 0

        if not risk_manager.check_position_limit(current_pos_amt, trend):
            print("仓位达到上限，跳过本次操作")
            time.sleep(60)
            continue

        qty_per_grid = risk_manager.calculate_order_quantity(
            usdt_balance,
            df['close'].iloc[-1],
            LONG_PARAMS['leverage'],
            TOTAL_CAPITAL_PCT,
            max_pos
        )

        grid_executor = GridExecutor(client, SYMBOL, max_pos)
        side = 'BUY' if trend == 'LONG' else 'SELL'
        grid_executor.place_grid_orders(side, fibo_levels, qty_per_grid)

        time.sleep(60)  # 1分钟周期循环

if __name__ == "__main__":
    main()
