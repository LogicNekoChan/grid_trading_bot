class RiskManager:
    def __init__(self, max_total_pos, capital_usage_ratio):
        self.max_total_pos = max_total_pos
        self.capital_usage_ratio = capital_usage_ratio

    def check_risk(self, current_pos_count, available_capital, price, quantity_per_order):
        """
        简单风险检查：
        - 当前持仓数量是否超过最大允许
        - 是否有足够资金挂单
        返回True/False
        """
        if current_pos_count >= self.max_total_pos:
            return False
        needed_capital = price * quantity_per_order
        if needed_capital > available_capital * self.capital_usage_ratio:
            return False
        return True
