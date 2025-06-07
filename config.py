# config.py
class Config:
    # Binance API
    API_KEY = "你的APIKEY"
    API_SECRET = "你的APISECRET"
    
    # 合约交易对
    SYMBOL = "BTCUSDC"
    
    # 杠杆和逐仓模式
    LEVERAGE = 10
    IS_ISOLATED = True  # 逐仓
    
    # EMA周期
    EMA_PERIODS = [20, 50, 200]
    
    # 斐波那契网格参数（以百分比）
    FIBO_LEVELS = [0.382, 0.5, 0.618, 1.0, 1.272, 1.618]
    GRID_NUM = 68
    GRID_SPACING_PERCENT = 0.36  # 网格间距百分比
    
    # 风控参数
    MAX_LONG_POS = 3   # 最大多仓网格持仓数
    MAX_SHORT_POS = 3  # 最大空仓网格持仓数
    MAX_TOTAL_POS = 6  # 最大总持仓数
    
    # 资金使用比例（现货资金百分比）
    CAPITAL_USAGE_RATIO = 0.8
    
    # 其他
    ORDER_TIMEOUT = 30  # 秒，挂单超时撤单重挂
    
    # 日志文件
    LOG_FILE = "logs/trade.log"
