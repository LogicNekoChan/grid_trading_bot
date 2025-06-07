import numpy as np

class FiboCalculator:
    def __init__(self, fibo_levels):
        self.fibo_levels = fibo_levels

    def calculate_grid_levels(self, low_price, high_price):
        """
        根据最低价最高价和斐波那契比例，计算网格价格列表
        返回一个升序的价格列表
        """
        price_range = high_price - low_price
        levels = [low_price + price_range * level for level in self.fibo_levels]
        return sorted(levels)

    def generate_grid_prices(self, low_price, high_price, grid_num):
        """
        根据网格数量和区间计算细分价格点
        """
        levels = self.calculate_grid_levels(low_price, high_price)
        grids = []
        # 简单线性插值细分（结合斐波那契区间也可以改进）
        for i in range(len(levels)-1):
            start = levels[i]
            end = levels[i+1]
            step = (end - start) / (grid_num // (len(levels)-1))
            for n in range(grid_num // (len(levels)-1)):
                grids.append(start + n * step)
        grids.append(levels[-1])
        return grids
