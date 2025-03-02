import random
import numpy as np
import pandas as pd

# ------------------ Giả lập hàm tính hiệu suất của công thức ------------------
def calculate_formula_performance(formula, data):
    """
    Giả lập tính các chỉ số hiệu suất cho công thức.
    Trong thực tế, hàm này sẽ chạy backtest trên dữ liệu lịch sử.
    
    Trả về:
      - sharpe: Chỉ số Sharpe
      - turnover: Tần suất giao dịch (trong khoảng 0 đến 1)
      - fitness: Một chỉ số tổng hợp của Returns, Sharpe và Turnover
      - drawdown: Mức giảm cao nhất (theo %)
      - returns: Lợi nhuận hàng năm (theo %)
    """
    sharpe = random.uniform(0.5, 3.0)         # Ví dụ: từ 0.5 đến 3.0
    turnover = random.uniform(0.005, 0.75)      # Một số giá trị có thể nằm ngoài phạm vi hợp lệ
    drawdown = random.uniform(2, 10)            # Giả lập: 2% đến 10%
    returns = random.uniform(5, 30)             # Lợi nhuận từ 5% đến 30%
    # Ví dụ, định nghĩa fitness = (Returns * Sharpe) / (Turnover + epsilon)
    fitness = (returns/100 * sharpe) / (turnover + 0.01)
    return sharpe, turnover, fitness, drawdown, returns

# ------------------ Hàm kiểm tra tiêu chí submit ------------------
def check_submission_criteria(sharpe, turnover, fitness, delay=1):
    """
    Kiểm tra xem các chỉ số có đạt đủ điều kiện submit hay không.
    
    - Với Delay = 1:
        + Sharpe phải >= 1.25
        + Fitness > 1.0
    - Với Delay = 0:
        + Sharpe phải >= 2.0
        + Fitness > 1.3
    - Turnover phải nằm trong khoảng từ 0.01 đến 0.70
    """
    if delay == 1:
        if sharpe < 1.25:
            return False
        if fitness <= 1.0:
            return False
    else:
        if sharpe < 2.0:
            return False
        if fitness <= 1.3:
            return False
    if not (0.01 <= turnover <= 0.70):
        return False
    return True

# ------------------ Hàm đánh giá công thức ------------------
def evaluate_formula(formula, data, delay=1):
    """
    Đánh giá công thức alpha dựa trên các chỉ số hiệu suất giả lập.
    
    Trả về một dictionary chứa:
      - formula: Công thức alpha
      - sharpe: Chỉ số Sharpe
      - turnover: Tần suất giao dịch
      - fitness: Chỉ số Fitness
      - drawdown: Mức Drawdown (theo %)
      - returns: Lợi nhuận hàng năm (theo %)
      - criteria_met: True nếu công thức vượt qua các tiêu chí, False nếu không.
    """
    sharpe, turnover, fitness, drawdown, returns = calculate_formula_performance(formula, data)
    criteria_met = check_submission_criteria(sharpe, turnover, fitness, delay)
    return {
        "formula": formula,
        "sharpe": sharpe,
        "turnover": turnover,
        "fitness": fitness,
        "drawdown": drawdown,
        "returns": returns,
        "criteria_met": criteria_met
    }

# ------------------ Ví dụ sử dụng ------------------
if __name__ == "__main__":
    # Giả sử data là DataFrame chứa dữ liệu lịch sử của alpha (ở đây dùng DataFrame rỗng cho ví dụ)
    data = pd.DataFrame()
    
    # Công thức mẫu (ví dụ được đưa ra)
    sample_formula = "power(assets_curr, equity) - group_rank(equity, 'industry') - group_zscore(sales, 'country')"
    
    # Đánh giá công thức với Delay = 1 (có thể thay đổi thành 0 nếu muốn)
    result = evaluate_formula(sample_formula, data, delay=1)
    
    # In kết quả
    print("Kết quả đánh giá công thức:")
    print(f"Công thức: {result['formula']}")
    print(f"Sharpe: {result['sharpe']:.2f}")
    print(f"Turnover: {result['turnover']:.2f}")
    print(f"Fitness: {result['fitness']:.2f}")
    print(f"Drawdown: {result['drawdown']:.2f}%")
    print(f"Returns: {result['returns']:.2f}%")
    print(f"Đạt tiêu chí submit: {result['criteria_met']}")
