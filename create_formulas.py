import random
import numpy as np
import pandas as pd

# ======================== Cấu hình tham số cho các hàm ========================
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
        "conditions": ["<", ">", "==", "!="],
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
    """Sinh tham số phù hợp cho từng hàm dựa trên FUNCTION_PARAMS."""
    params = FUNCTION_PARAMS.get(func_name, {})
    
    # Xử lý số lượng đối số nếu 'args' được định nghĩa dưới dạng chuỗi (ví dụ ">=2")
    if isinstance(params.get("args"), str) and params["args"].startswith(">="):
        min_args = int(params["args"][2:])
        num_args = min_args  # có thể điều chỉnh thêm nếu muốn sinh thêm đối số
    else:
        num_args = params.get("args", 1)
    
    # --- Arithmetic functions có filter_param ---
    if params.get("filter_param", False) and func_name in ["add", "subtract", "multiply"]:
        # Sinh ra 2 cột và thêm tham số filter
        args = [random.choice(columns) for _ in range(2)]
        args.append(f"filter={random.choice(['true', 'false'])}")
        return args
    
    # --- Time Series functions ---
    elif func_name.startswith("ts_"):
        # Xử lý riêng cho ts_regression vì yêu cầu 4 đối số
        if func_name == "ts_regression":
            window = random.randint(5, 252)
            return [random.choice(columns), random.choice(columns), window, 0]  # sử dụng lag=0 theo mặc định
        else:
            col = random.choice(columns)
            if "window_range" in params:
                window = random.randint(*params["window_range"])
                if func_name == "ts_corr":
                    # ts_corr yêu cầu 3 đối số: (x, y, d)
                    return [col, random.choice(columns), window]
                return [col, window]
            else:
                return [col]
    
    # --- Logical functions ---
    elif func_name in ["and", "or"]:
        return [random.choice(columns) for _ in range(2)]
    elif func_name in ["not", "is_nan"]:
        return [random.choice(columns)]
    elif func_name == "if_else":
        conditions = params.get("conditions", ["<", ">", "==", "!="])
        condition = f"{random.choice(columns)} {random.choice(conditions)} {random.choice(columns)}"
        return [condition, random.choice(columns), random.choice(columns)]
    
    # --- Cross Sectional and Vector functions ---
    # Các hàm này nhận 1 đối số
    elif func_name in ["normalize", "quantile", "rank", "scale", "winsorize", "zscore", "vec_avg", "vec_sum"]:
        return [random.choice(columns)]
    
    # --- Transformational functions ---
    elif func_name == "bucket":
        return [random.choice(columns)]
    elif func_name == "trade_when":
        # Cần 3 đối số
        return [random.choice(columns) for _ in range(3)]
    
    # --- Group functions ---
    elif func_name.startswith("group_"):
        # Với group_mean và group_backfill cần 3 đối số: (x, weight, group)
        if func_name in ["group_mean", "group_backfill"]:
            groups = FUNCTION_PARAMS.get(func_name, {}).get("default", {}).get("group")
            if groups is None:
                groups = ["sector", "industry", "country"]
            return [random.choice(columns), random.choice(columns), f"'{random.choice(groups)}'"]
        else:
            # Các hàm group khác (group_neutralize, group_rank, group_zscore) yêu cầu 2 đối số: (x, group)
            groups = FUNCTION_PARAMS.get(func_name, {}).get("default", {}).get("group")
            if groups is None:
                groups = ["sector", "industry", "country"]
            return [random.choice(columns), f"'{random.choice(groups)}'"]
    
    # --- Default: nếu không thuộc các trường hợp đặc biệt, sinh num_args đối số từ columns ---
    else:
        return [random.choice(columns) for _ in range(num_args)]

# ======================== Hàm sinh lệnh gọi hàm ========================
def generate_function_call(func_name, columns):
    """Tạo lệnh gọi hàm với cú pháp chính xác dựa trên các tham số sinh ra."""
    args = generate_arguments(func_name, columns)
    formatted_args = []
    for arg in args:
        if isinstance(arg, str):
            formatted_args.append(arg)
        else:
            formatted_args.append(str(arg))
    return f"{func_name}({', '.join(formatted_args)})"

# ======================== Hàm sinh công thức ngẫu nhiên ========================
def generate_random_formula(columns, max_depth=2):
    """
    Sinh công thức alpha ngẫu nhiên với độ phức tạp kiểm soát dựa trên FUNCTION_PARAMS.
    
    Parameters:
      - columns: danh sách tên cột có sẵn (ví dụ: ['assets_curr', 'equity', 'sales'])
      - max_depth: độ sâu của công thức (cho phép kết hợp với toán tử)
      
    Trả về:
      - Một chuỗi biểu thức đại diện cho công thức alpha.
    """
    # Định nghĩa ánh xạ nhóm hàm (category) với danh sách tên hàm theo FUNCTION_PARAMS
    categories = {
        "Arithmetic": ["abs", "add", "densify", "divide", "inverse", "log", "max", "min", "multiply", "power", "reverse", "sign", "signed_power", "subtract"],
        "Logical": ["and", "if_else", "is_nan", "not", "or"],
        "TimeSeries": ["days_from_last_change", "hump", "kth_element", "last_diff_value", "ts_arg_max", "ts_arg_min", "ts_av_diff", "ts_backfill",
                       "ts_corr", "ts_count_nans", "ts_covariance", "ts_decay_linear", "ts_delay", "ts_delta", "ts_mean", "ts_product",
                       "ts_quantile", "ts_rank", "ts_regression", "ts_scale", "ts_std_dev", "ts_step", "ts_sum", "ts_zscore"],
        "CrossSectional": ["normalize", "quantile", "rank", "scale", "winsorize", "zscore"],
        "Vector": ["vec_avg", "vec_sum"],
        "Transformational": ["bucket", "trade_when"],
        "Group": ["group_backfill", "group_mean", "group_neutralize", "group_rank", "group_zscore"]
    }
    
    # Nếu độ sâu đã hết, chỉ trả về một cột ngẫu nhiên
    if max_depth <= 0:
        return random.choice(columns)
    
    # Chọn ngẫu nhiên một nhóm hàm
    chosen_category = random.choice(list(categories.keys()))
    # Chọn ngẫu nhiên một hàm từ nhóm đó
    func = random.choice(categories[chosen_category])
    
    # Sinh lệnh gọi hàm (function call) dựa trên tên hàm đã chọn và danh sách columns
    expr = generate_function_call(func, columns)
    
    # Với một xác suất (ví dụ 50%) và nếu độ sâu > 1, kết hợp biểu thức với toán tử và công thức con
    if random.random() < 0.5 and max_depth > 1:
        operator = random.choice(["+", "-", "*"])
        return f"{expr} {operator} {generate_random_formula(columns, max_depth - 1)}"
    
    return expr

# ======================== Sử dụng ========================
if __name__ == "__main__":
    columns = ['assets_curr', 'equity', 'sales']
    output = []
    
    # Sinh 100 công thức
    for _ in range(100):
        formula = generate_random_formula(columns, max_depth=random.randint(0, 4))
        output.append(formula)
    
    # Ghi vào file
    with open("alpha_formulas.txt", "a+") as f:
        for expr in output:
            f.write("STATUS: YET TO USE\n")
            f.write(f"  {expr}\n\n")

    print("___ DONE ___")
