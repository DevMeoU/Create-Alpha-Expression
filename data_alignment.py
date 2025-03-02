import random
import pandas as pd
import numpy as np

# ======================== CẤU HÌNH TIÊU CHÍ ========================
TARGET_CRITERIA = {
    "Sharpe >= 1.25": True,
    "Drawdown <= 5%": True,
    "Turnover 1%-70%": True
}

# ======================== ĐỊNH NGHĨA HÀM HỖ TRỢ ========================
def ts_corr(x, y, d):
    """Tính rolling correlation giữa 2 chuỗi với cửa sổ d ngày."""
    return x.rolling(window=d).corr(y)

def ts_arg_min(x, d):
    """
    Trả về series với giá trị 1 nếu giá trị cuối của cửa sổ rolling bằng giá trị nhỏ nhất trong cửa sổ, 0 còn lại.
    Đây là một cách để tạo tín hiệu từ chuỗi.
    """
    return x.rolling(window=d).apply(lambda s: 1 if s.iloc[-1] == s.min() else 0, raw=False)

def group_zscore(x, group):
    """Tính z-score của chuỗi x. Ở đây bỏ qua tham số group."""
    return (x - x.mean()) / x.std()

def scale(x, scale=0.9):
    """Nhân chuỗi x với hệ số scale."""
    return x * scale

def winsorize(x, std=3):
    """Winsorize chuỗi x bằng cách cắt bớt giá trị ngoài khoảng [mean - std*std, mean + std*std]."""
    mean_val = x.mean()
    std_val = x.std()
    lower = mean_val - std * std_val
    upper = mean_val + std * std_val
    return x.clip(lower, upper)

# ======================== HÀM TÍNH HIỆU SUẤT CÔNG THỨC ========================
def calculate_formula_performance(formula, data):
    """
    Đánh giá hiệu suất của công thức bằng cách:
      - Dùng eval() để tính chuỗi tín hiệu alpha từ công thức.
      - Tính lợi nhuận giao dịch dựa trên tín hiệu đó (sử dụng phần % thay đổi của giá Close).
      - Tính Sharpe ratio, max drawdown và turnover của tín hiệu.
    """
    # Xây dựng context cho eval(): bao gồm các hàm và các cột dữ liệu
    context = {
        'ts_corr': ts_corr,
        'ts_arg_min': ts_arg_min,
        'group_zscore': group_zscore,
        'scale': scale,
        'winsorize': winsorize,
        'np': np,
        'pd': pd,
        'random': random
    }
    for col in data.columns:
        context[col] = data[col]
        
    # Đánh giá công thức để nhận được tín hiệu alpha
    try:
        alpha_signal = eval(formula, context)
    except Exception as e:
        print("Error evaluating formula:", e)
        raise e
        
    # Đảm bảo alpha_signal là một Series có index giống với data
    if not isinstance(alpha_signal, pd.Series):
        alpha_signal = pd.Series(alpha_signal, index=data.index)
    else:
        alpha_signal = alpha_signal.reindex(data.index).ffill()
    
    # Tính lợi nhuận hàng ngày từ giá Close
    returns = data["Close"].pct_change().dropna()
    # Căn chỉnh tín hiệu alpha với returns; giả sử tín hiệu được dùng cho ngày kế tiếp
    alpha_signal = alpha_signal.reindex(returns.index).ffill()
    strat_returns = alpha_signal.shift(1) * returns
    
    # Tính Sharpe ratio annualized (giả sử 252 ngày giao dịch)
    if strat_returns.std() != 0:
        sharpe = (strat_returns.mean() / strat_returns.std()) * np.sqrt(252)
    else:
        sharpe = 0
    
    # Tính max drawdown
    cum_returns = (1 + strat_returns).cumprod()
    roll_max = cum_returns.cummax()
    drawdown_series = (cum_returns - roll_max) / roll_max
    max_drawdown = drawdown_series.min()  # giá trị âm
    drawdown_percent = abs(max_drawdown) * 100  # chuyển sang %
    
    # Tính turnover: trung bình biến động ngày-to-day của tín hiệu
    turnover = alpha_signal.diff().abs().mean()
    
    return sharpe, drawdown_percent, turnover

def check_criteria(sharpe, drawdown, turnover):
    """So sánh các chỉ số hiệu suất với tiêu chí mục tiêu."""
    criteria = {
        "Sharpe >= 1.25": sharpe >= 1.25,
        "Drawdown <= 5%": drawdown <= 5,
        "Turnover 1%-70%": (0.01 <= turnover <= 0.70)
    }
    return criteria

# ======================== HÀM SINH CÔNG THỨC ========================
def generate_optimized_formula(columns):
    """Sinh công thức ngẫu nhiên với cấu trúc tối ưu dựa trên các cột của dữ liệu."""
    base_ops = [
        lambda: f"rank({random.choice(columns)}, {random.choice(columns)}, {random.randint(30, 180)})",
        lambda: f"ts_corr({random.choice(columns)}, {random.choice(columns)}, {random.randint(30, 180)})",
        lambda: f"ts_arg_min({random.choice(columns)}, {random.randint(20, 60)})",
        lambda: f"group_zscore({random.choice(columns)}, '{random.choice(['sector','industry'])}')"
    ]
    
    modifiers = [
        lambda x: f"scale({x}, scale=0.9)",
        lambda x: f"winsorize({x}, std=3)",
        lambda x: f"({x}) * {random.uniform(0.8, 1.2):.2f}"
    ]
    
    formula = random.choice(base_ops)()
    for _ in range(random.randint(0, 2)):
        formula = random.choice(modifiers)(formula)
        
    return formula

def evaluate_formula(formula_func, data, max_trials=100):
    """Sinh và đánh giá nhiều công thức cho đến khi đạt tiêu chí, trả về công thức tốt nhất và điểm số của nó."""
    best_score = -np.inf
    best_formula = None
    
    for _ in range(max_trials):
        current_formula = formula_func(data.columns.tolist())
        try:
            sharpe, drawdown, turnover = calculate_formula_performance(current_formula, data)
            # Tính điểm tổng hợp (score): sử dụng trọng số cho từng chỉ số
            score = (sharpe * 0.5) + (-abs(drawdown) * 0.3) + ((1 - abs(turnover - 0.35)) * 0.2)
            crit = check_criteria(sharpe, drawdown, turnover)
            if crit == TARGET_CRITERIA and score > best_score:
                best_score = score
                best_formula = current_formula
                print(f"Đạt tiêu chí với formula: {current_formula} | Sharpe: {sharpe:.2f}, Drawdown: {drawdown:.2f}%, Turnover: {turnover:.2f}, Score: {score:.2f}")
        except Exception as e:
            continue
            
    return best_formula, best_score

# ======================== CHƯƠNG TRÌNH CHÍNH ========================
if __name__ == "__main__":
    # Load dữ liệu từ file Excel; giả sử cột 't' được đổi tên thành "Date" hoặc giữ là 't'
    # Ở đây, chúng ta dùng cột 't' làm index
    data = pd.read_excel("AAPL_stock_data.xlsx", parse_dates=["t"], index_col="t")
    
    best_formula, best_score = evaluate_formula(
        generate_optimized_formula,
        data,
        max_trials=500
    )
    
    print(f"Công thức tốt nhất: {best_formula}")
    print(f"Điểm đánh giá: {best_score:.2f}")
    
    # Lưu kết quả vào file
    with open("optimized_formulas.txt", "w") as f:
        f.write(f"Best Formula: {best_formula}\n")
        f.write(f"Validation Score: {best_score:.2f}\n")
        f.write("Passed Criteria:\n")
        sharpe, drawdown, turnover = calculate_formula_performance(best_formula, data)
        for criterion, status in check_criteria(sharpe, drawdown, turnover).items():
            if status:
                f.write(f"- {criterion}\n")
