import random
import numpy as np
import pandas as pd

# ======================== Cấu hình hàm và tham số =========================
FUNCTION_PARAMS = {
    # Arithmetic functions
    "abs": {
        "args": 1,
        "description": "Tính giá trị tuyệt đối của x."
    },
    "add": {
        "args": ">=2",   # Yêu cầu ít nhất 2 đối số
        "variadic": True,
        "filter_param": True,
        "description": "Cộng các input (>=2). Nếu filter=true, giá trị NaN được chuyển thành 0 trước khi cộng."
    },
    "densify": {
        "args": 1,
        "description": "Chuyển đổi một trường phân nhóm có nhiều bucket thành số bucket ít hơn để tăng hiệu quả tính toán."
    },
    "divide": {
        "args": 2,
        "description": "Chia x cho y."
    },
    "inverse": {
        "args": 1,
        "description": "Tính nghịch đảo 1/x."
    },
    "log": {
        "args": 1,
        "description": "Tính logarit tự nhiên của x."
    },
    "max": {
        "args": ">=2",
        "description": "Trả về giá trị lớn nhất trong các input (cần ít nhất 2 input)."
    },
    "min": {
        "args": ">=2",
        "description": "Trả về giá trị nhỏ nhất trong các input (cần ít nhất 2 input)."
    },
    "multiply": {
        "args": ">=2",
        "variadic": True,
        "filter_param": True,
        "description": "Nhân tất cả các input (>=2). Nếu filter=true, giá trị NaN được chuyển thành 1."
    },
    "power": {
        "args": 2,
        "description": "Tính lũy thừa: x^y."
    },
    "reverse": {
        "args": 1,
        "description": "Trả về giá trị âm của x (-x)."
    },
    "sign": {
        "args": 1,
        "description": "Trả về dấu của x; nếu x là NaN thì trả về NaN."
    },
    "signed_power": {
        "args": 2,
        "description": "Tính x^y nhưng giữ lại dấu của x."
    },
    "subtract": {
        "args": ">=2",
        "variadic": True,
        "filter_param": True,
        "description": "Trừ các input; nếu filter=true, giá trị NaN chuyển thành 0 trước khi trừ."
    },

    # Logical functions
    "and": {
        "args": 2,
        "description": "Toán tử AND logic; trả về True nếu cả 2 đối số đều đúng."
    },
    "if_else": {
        "args": 3,
        "description": "Nếu input1 đúng thì trả về input2, ngược lại trả về input3."
    },
    "is_nan": {
        "args": 1,
        "description": "Trả về 1 nếu input là NaN, ngược lại trả về 0."
    },
    "not": {
        "args": 1,
        "description": "Trả về phủ định của x: nếu x đúng (1) trả về 0, nếu x sai (0) trả về 1."
    },
    "or": {
        "args": 2,
        "description": "Toán tử OR logic; trả về True nếu một trong hai đối số đúng."
    },

    # Time Series functions
    "days_from_last_change": {
        "args": 1,
        "description": "Trả về số ngày kể từ khi giá trị của x thay đổi lần cuối."
    },
    "hump": {
        "args": 1,
        "default": {"hump": 0.01},
        "description": "Giới hạn mức độ thay đổi của x nhằm giảm turnover, với tham số hump xác định ngưỡng thay đổi."
    },
    "kth_element": {
        "args": 3,
        "description": "Trả về phần tử thứ k của x trong khoảng lookback d ngày."
    },
    "last_diff_value": {
        "args": 2,
        "description": "Trả về giá trị cuối cùng của x trong d ngày trước đó mà khác với giá trị hiện tại."
    },
    "ts_arg_max": {
        "args": 2,
        "window_range": (5, 252),
        "description": "Trả về chỉ số tương đối của giá trị lớn nhất trong x trong khoảng d ngày; nếu giá trị lớn nhất xảy ra ngày hiện tại, trả về 0."
    },
    "ts_arg_min": {
        "args": 2,
        "window_range": (5, 252),
        "description": "Trả về chỉ số tương đối của giá trị nhỏ nhất trong x trong khoảng d ngày; nếu giá trị nhỏ nhất xảy ra ngày hiện tại, trả về 0."
    },
    "ts_av_diff": {
        "args": 2,
        "description": "Trả về hiệu của x và trung bình trượt của x trong khoảng d ngày (bỏ qua NaN)."
    },
    "ts_backfill": {
        "args": 3,
        "default": {"lookback": "d", "k": 1, "ignore": "NAN"},
        "description": "Thay thế các giá trị NaN hoặc 0 của x bằng giá trị không phải NaN đầu tiên tìm được trong khoảng lookback d ngày."
    },
    "ts_corr": {
        "args": 3,
        "window_range": (5, 252),
        "description": "Tính hệ số tương quan giữa x và y trong khoảng d ngày."
    },
    "ts_count_nans": {
        "args": 2,
        "description": "Đếm số lượng giá trị NaN trong x trong khoảng d ngày."
    },
    "ts_covariance": {
        "args": 3,
        "description": "Tính hiệp phương sai giữa y và x trong khoảng d ngày."
    },
    "ts_decay_linear": {
        "args": 3,
        "default": {"dense": False},
        "description": "Áp dụng decay tuyến tính lên x trong khoảng d ngày; dense=False có nghĩa là NaN được coi là 0."
    },
    "ts_delay": {
        "args": 2,
        "description": "Trả về giá trị của x cách đây d ngày."
    },
    "ts_delta": {
        "args": 2,
        "description": "Trả về hiệu giữa x hiện tại và giá trị của x d ngày trước đó (x - ts_delay(x,d))."
    },
    "ts_mean": {
        "args": 2,
        "window_range": (5, 252),
        "description": "Trả về trung bình của x trong khoảng d ngày."
    },
    "ts_product": {
        "args": 2,
        "description": "Trả về tích của các giá trị x trong khoảng d ngày."
    },
    "ts_quantile": {
        "args": 3,
        "default": {"driver": "gaussian"},
        "description": "Tính ts_rank sau đó áp dụng hàm phân phối ngược từ driver (mặc định gaussian)."
    },
    "ts_rank": {
        "args": 2,
        "default": {"constant": 0},
        "description": "Xếp hạng các giá trị của x trong khoảng d ngày; trả về thứ hạng của giá trị hiện tại."
    },
    "ts_regression": {
        "args": 4,
        "default": {"lag": 0, "rettype": 0},
        "description": "Thực hiện hồi quy của y theo x trong khoảng d ngày, trả về tham số theo kiểu trả về (rettype)."
    },
    "ts_scale": {
        "args": 3,
        "default": {"constant": 0},
        "description": "Chuẩn hóa x trong khoảng d ngày theo công thức: (x - ts_min(x,d))/(ts_max(x,d)-ts_min(x,d)) + constant."
    },
    "ts_std_dev": {
        "args": 2,
        "description": "Trả về độ lệch chuẩn của x trong khoảng d ngày."
    },
    "ts_step": {
        "args": 1,
        "description": "Trả về bộ đếm ngày (step) trong chuỗi thời gian."
    },
    "ts_sum": {
        "args": 2,
        "description": "Trả về tổng của x trong khoảng d ngày."
    },
    "ts_zscore": {
        "args": 2,
        "description": "Tính z-score cho x trong khoảng d ngày: (x - mean)/std."
    },

    # Cross Sectional functions
    "normalize": {
        "args": 1,
        "default": {"useStd": False, "limit": 0.0},
        "description": "Trung hòa giá trị của x theo từng ngày bằng cách trừ đi trung bình (và nếu useStd=True thì chia cho độ lệch chuẩn)."
    },
    "quantile": {
        "args": 1,
        "default": {"driver": "gaussian", "sigma": 1.0},
        "description": "Xếp hạng x sau đó áp dụng biến đổi phân phối (mặc định gaussian)."
    },
    "rank": {
        "args": 1,
        "default": {"rate": 2},
        "description": "Xếp hạng x giữa các công cụ, trả về giá trị trong khoảng [0,1]."
    },
    "scale": {
        "args": 1,
        "default": {"scale": 1, "longscale": 1, "shortscale": 1},
        "description": "Chuyển đổi giá trị của x theo quy mô (scale) cho vị thế booksize, long và short."
    },
    "winsorize": {
        "args": 1,
        "default": {"std": 4},
        "description": "Giới hạn giá trị của x trong khoảng [mean - 4*std, mean + 4*std]."
    },
    "zscore": {
        "args": 1,
        "description": "Tính z-score cho x trên toàn bộ cross-section (x - mean)/std."
    },

    # Vector functions
    "vec_avg": {
        "args": 1,
        "description": "Trung bình của một trường vector."
    },
    "vec_sum": {
        "args": 1,
        "description": "Tổng của một trường vector."
    },

    # Transformational functions
    "bucket": {
        "args": 1,
        "default": {"range": "0,1,0.1", "buckets": None},
        "description": "Chuyển đổi giá trị float của x thành các bucket rời rạc theo khoảng cho trước hoặc danh sách bucket."
    },
    "trade_when": {
        "args": 3,
        "description": "Cập nhật giá trị alpha của x chỉ khi điều kiện y được thỏa mãn, ngược lại giữ nguyên hoặc đóng vị thế."
    },

    # Group functions
    "group_backfill": {
        "args": 3,
        "default": {"std": 4.0},
        "description": "Thay thế giá trị NaN của x bằng giá trị trung bình đã winsorize của các công cụ cùng nhóm trong khoảng d ngày."
    },
    "group_mean": {
        "args": 3,
        "description": "Tính trung bình của x trong nhóm, có thể có trọng số (weight)."
    },
    "group_neutralize": {
        "args": 2,
        "default": {"group": ["sector", "industry", "country"]},
        "description": "Trung hòa giá trị của x đối với nhóm (ví dụ: ngành, quốc gia, ...)."
    },
    "group_rank": {
        "args": 2,
        "description": "Xếp hạng x trong mỗi nhóm."
    },
    "group_zscore": {
        "args": 2,
        "default": {"group": None},
        "description": "Tính z-score của x trong từng nhóm (x - mean)/std cho từng nhóm."
    }
}

# ======================== Hàm sinh tham số ========================
def generate_arguments(func_name, columns):
    """Sinh tham số phù hợp cho từng hàm"""
    params = FUNCTION_PARAMS.get(func_name, {})
    
    # Xử lý hàm có số tham số cố định
    if func_name in ["add", "subtract", "multiply", "divide"]:
        args = [random.choice(columns) for _ in range(2)]
        if params.get("filter_param"):
            args.append(f"filter={random.choice(['true', 'false'])}")
        return args
    
    # Xử lý hàm time series
    elif func_name.startswith("ts_"):
        col = random.choice(columns)
        window = random.randint(*params.get("window_range", (5, 252)))
        if func_name == "ts_corr":
            return [col, random.choice(columns), window]
        return [col, window]
    
    # Xử lý hàm if_else
    elif func_name == "if_else":
        condition = f"{random.choice(columns)} {random.choice(params['conditions'])} {random.choice(columns)}"
        return [condition, random.choice(columns), random.choice(columns)]
    
    # Xử lý hàm group
    elif func_name.startswith("group_"):
        return [random.choice(columns), f"'{random.choice(params['groups'])}'"]
    
    # Mặc định: 1 tham số
    return [random.choice(columns)]

# ======================== Hàm sinh công thức ========================
def generate_function_call(func_name, columns):
    """Tạo lệnh gọi hàm với cú pháp chính xác"""
    args = generate_arguments(func_name, columns)
    
    # Định dạng tham số
    formatted_args = []
    for arg in args:
        if isinstance(arg, str) and "'" in arg:  # Xử lý chuỗi
            formatted_args.append(arg)
        else:
            formatted_args.append(str(arg))
    
    return f"{func_name}({', '.join(formatted_args)})"

def generate_random_formula(columns, max_depth=2):
    """Sinh công thức với độ phức tạp có kiểm soát"""
    if max_depth <= 0:
        return random.choice(columns)
    
    # Chọn loại hàm
    func_type = random.choice(["arithmetic", "timeseries", "logical", "group"])
    
    # Sinh biểu thức
    if func_type == "arithmetic":
        func = random.choice(["add", "subtract", "multiply", "power"])
        expr = generate_function_call(func, columns)
    elif func_type == "timeseries":
        func = random.choice(["ts_arg_min", "ts_mean", "ts_corr"])
        expr = generate_function_call(func, columns)
    elif func_type == "logical":
        expr = generate_function_call("if_else", columns)
    else:
        func = random.choice(["group_neutralize", "group_zscore"])
        expr = generate_function_call(func, columns)
    
    # Thêm toán tử kết hợp
    if random.random() < 0.5 and max_depth > 1:
        operator = random.choice(["+", "-", "*"])
        return f"{expr} {operator} {generate_random_formula(columns, max_depth-1)}"
    
    return expr

# ======================== Sử dụng ========================
if __name__ == "__main__":
    columns = ['assets_curr', 'equity', 'sales']
    output = []
    
    # Sinh 20 công thức
    for _ in range(100):
        formula = generate_random_formula(columns)
        output.append(formula)

    # Ghi vào file
    with open("alpha_formulas.txt", "a+") as f:
        for expr in output:
            f.write("STATUS: YET TO USE\n")
            f.write(f"  {expr}\n\n")

    print("___ DONE ___")
# Kết quả mẫu:
"""
ts_arg_min(assets_curr, 189) * 0.75
group_zscore('equity', 'sector') - ts_mean(sales, 42)
if_else(assets_curr < equity, ts_corr(sales, equity, 120), power(assets_curr, 2)) 
add(equity, sales, filter=true) * 1.2
ts_arg_max(sales, 75) + group_neutralize('assets_curr', 'industry')
"""