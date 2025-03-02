import random
import numpy as np
import pandas as pd
from random import choice, randint

# --------------------------
# Các hàm hỗ trợ cơ bản
# --------------------------
def subtract(a, b, filter=False):
    return a - b

def ts_arg_min(series, window):
    return series.rolling(window=window).apply(lambda x: x.argmin())

def hump(series, hump=0.01):
    return np.sign(series) + hump

def rank(series):
    return series.rank(pct=True)

# --------------------------
# Generator công thức ngẫu nhiên
# --------------------------
class AlphaFormulaGenerator:
    def __init__(self):
        self.metrics = ['assets_curr', 'equity', 'sales', 'ebitda', 'cash_flow', 'liabilities']
        self.operations = ['subtract', 'add', 'multiply']
        self.ts_functions = ['ts_arg_min', 'ts_arg_max', 'rolling_mean']
        self.transformations = ['hump', 'log', 'abs']
        self.windows = [50, 100, 189, 200]  # Các cửa sổ thời gian phổ biến
    
    def _random_component(self):
        # Random chọn 1 thành phần trong công thức
        component_type = choice(['basic', 'ts', 'transformed'])
        
        if component_type == 'basic':
            return choice(self.metrics)
        
        elif component_type == 'ts':
            ts_func = choice(self.ts_functions)
            metric = choice(self.metrics)
            window = choice(self.windows)
            return f"{ts_func}({metric}, {window})"
        
        elif component_type == 'transformed':
            transform = choice(self.transformations)
            base = self._random_component()
            if transform == 'hump':
                return f"{transform}({base}, hump={np.round(np.random.uniform(0.01, 0.1), 2)})"
            return f"{transform}({base})"
    
    def generate_formula(self, num_terms=3):
        terms = []
        for _ in range(num_terms):
            # 50% cơ hội có phép toán phức tạp
            if np.random.rand() > 0.5:
                op = choice(self.operations)
                a = self._random_component()
                b = self._random_component()
                term = f"{op}({a}, {b}, filter=false)"
            else:
                term = self._random_component()
            
            terms.append(f"rank({term})")
        
        return " + ".join(terms)

# --------------------------
# Ví dụ sử dụng
# --------------------------
if __name__ == "__main__":
    np.random.seed(42)
    
    # Khởi tạo generator
    generator = AlphaFormulaGenerator()
    
    # Sinh 3 công thức ngẫu nhiên
    for _ in range(3):
        formula = generator.generate_formula()
        print("Công thức sinh ra:")
        print(formula)
        print("\n" + "-"*50 + "\n")
    
    # Giả định DataFrame dữ liệu
    data = pd.DataFrame({
        'assets_curr': np.random.normal(100, 20, 1000),
        'equity': np.random.normal(50, 10, 1000),
        'sales': np.random.normal(200, 50, 1000),
        'profit': np.random.normal(100, 20, 1000),
        'profit_margin': np.random.normal(50, 10, 1000),
        'asset_turnover': np.random.normal(200, 50, 1000)
    })
    
    # Áp dụng 1 công thức mẫu
    # example_formula = "rank(subtract(assets_curr, equity, filter=false)) + rank(ts_arg_min(sales, 189))"
    from create_formula import generate_random_formula
    example_formula = generate_random_formula(num_expressions=random.randint(1, 3))
    print(f"example_formula: {example_formula}")
    
    # Tính toán
    data['net_assets'] = subtract(data['assets_curr'], data['equity'])
    data['sales_min_pos'] = ts_arg_min(data['sales'], 189)
    
    data['alpha'] = rank(data['net_assets']) + rank(data['sales_min_pos'])
    print(data[['assets_curr', 'equity', 'sales', 'alpha']].head())

# ```

# ### Kết quả mẫu:
# ```
# Công thức sinh ra:
# rank(hump(ts_arg_max(ebitda, 189), hump=0.07)) + rank(add(rolling_mean(liabilities, 50), cash_flow, filter=false)) + rank(abs(ts_arg_min(equity, 200)))

# --------------------------------------------------

# Công thức sinh ra:
# rank(subtract(assets_curr, ts_arg_min(ebitda, 100), filter=false)) + rank(add(equity, hump(sales, hump=0.03), filter=false)) + rank(ts_arg_max(rolling_mean(liabilities, 200), 189))

# --------------------------------------------------
# ```

""" ### Giải thích:
1. **Cấu trúc công thức**:
   - Kết hợp ngẫu nhiên các **phép toán** (subtract/add/multiply)
   - **Time-series functions** (ts_arg_min, rolling_mean)
   - **Biến đổi** (hump, log, abs)
   - **Ranking** cho từng thành phần

2. **Tùy biến**:
   - Thêm/sửa các metrics trong `self.metrics`
   - Điều chỉnh xác suất phức tạp qua `num_terms` và tỷ lệ trong `generate_formula()`
   - Thêm hàm mới vào `self.ts_functions` hoặc `self.transformations`

3. **Áp dụng thực tế**:
   - Kết nối dữ liệu thực từ CSV/API
   - Thêm validation để đảm bảo công thức hợp lệ
   - Kết hợp backtesting để đánh giá hiệu quả alpha

Bạn có thể mở rộng code này để sinh ra hàng nghìn công thức khác nhau và kiểm tra hiệu suất của chúng trên dữ liệu lịch sử! 
### """