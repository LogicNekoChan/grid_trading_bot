import time
import pandas as pd
from config import Config
from binance_futures import BinanceFuturesClient
from trend_detector import TrendDetector
from fibo_calculator import FiboCalculator
from grid_executor import GridExecutor
from risk_manager import RiskManager

def main():
    cfg = Config()
    client = BinanceFuturesClient(cfg.API_KEY, cfg.API_SECRET, cfg.SYMBOL, cfg.LEVERAGE, cfg.IS_ISOLATED)
    trend_detector = TrendDetector(cfg.EMA_PERIODS)
    fibo_calc = FiboCalculator(cfg.FIBO_LEVELS)
    grid_executor = GridExecutor(client, cfg.MAX_LONG_POS, cfg.MAX_SHORT_POS)
    risk_manager = RiskManager(cfg.MAX_TOTAL_POS, cfg.CAPITAL_USAGE_RATIO)

    while True:
        klines_raw = client.get_klines('1d', 200)
        # 转换为DataFrame，假设binance返回列表
        klines = pd.DataFrame(klines_raw, columns=['open_time', 'open', 'high', 'low', 'close', 'volume',
                                                  'close_time', 'quote_asset_volume', 'number_of_trades',
                                                  'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        klines['close'] = klines['close'].astype(float)
        klines['high'] = klines['high'].astype(float)
        klines['low'] = klines['low'].astype(float)

        trend = trend_detector.detect_trend(klines)

        low_price = klines['low'].min()
        high_price = klines['high'].max()
        grid_prices = fibo_calc.generate_grid_prices(low_price, high_price, cfg.GRID_NUM)

        available_capital = client.get_account_balance()
        quantity_per_order = 0.001  # 示例，后续可改为动态计算

        if trend == "long":
            # 做多网格策略
            if risk_manager.check_risk(0, available_capital, grid_prices[0], quantity_per_order):
                grid_executor.place_grid_orders(grid_prices, "LONG", quantity_per_order)
        elif trend == "short":
            # 做空网格策略
            if risk_manager.check_risk(0, available_capital, grid_prices[-1], quantity_per_order):
                grid_executor.place_grid_orders(grid_prices, "SHORT", quantity_per_order)
        else:
            print("当前趋势中性，等待")

        time.sleep(60)  # 每分钟运行一次

if __name__ == '__main__':
    main()
