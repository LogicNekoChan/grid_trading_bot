import numpy as np
import pandas as pd

class TrendDetector:
    def __init__(self, ema_periods):
        self.ema_periods = ema_periods

    def calculate_ema(self, prices, period):
        return prices.ewm(span=period, adjust=False).mean()

    def detect_trend(self, klines):
        """
        klines: DataFrame，至少含有 'close' 列
        返回：多空趋势信号 "long" / "short" / "neutral"
        """
        close = klines['close']
        ema20 = self.calculate_ema(close, self.ema_periods[0])
        ema50 = self.calculate_ema(close, self.ema_periods[1])
        ema200 = self.calculate_ema(close, self.ema_periods[2])

        # 简单趋势判断规则：
        # 多头趋势：EMA20 > EMA50 > EMA200
        # 空头趋势：EMA20 < EMA50 < EMA200
        # 其他中性
        if ema20.iloc[-1] > ema50.iloc[-1] > ema200.iloc[-1]:
            return "long"
        elif ema20.iloc[-1] < ema50.iloc[-1] < ema200.iloc[-1]:
            return "short"
        else:
            return "neutral"
