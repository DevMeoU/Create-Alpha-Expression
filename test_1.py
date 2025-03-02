def evaluate_alpha_metrics(metrics, delay=1):
    """
    Đánh giá các chỉ số hiệu suất của một alpha dựa trên các tiêu chí:
      - Sharpe: Delay=1 phải >1.25; Delay=0 phải >2.0
      - Turnover: phải từ 1% đến 70% (0.01 đến 0.70)
      - Fitness: Delay=1 phải >1.0; Delay=0 phải >1.3
      - (Các chỉ số Returns, Drawdown, Margin cũng có thể được thêm vào nếu cần)
      
    Input:
      metrics: dict chứa các chỉ số, ví dụ:
               {
                 "Sharpe": 1.1,
                 "Turnover": 0.05,
                 "Fitness": 0.9,
                 "Drawdown": 3.0,    # tính theo %
                 "Returns": 7.0,     # tính theo %
                 "Margin": 60.0
               }
      delay: 0 hoặc 1, xác định loại alpha (Delay=0 hay Delay=1)
      
    Output:
      Một dict gồm:
         - passed: True/False
         - suggestions: Danh sách các gợi ý điều chỉnh nếu không đạt
         - metrics: Các chỉ số đã đánh giá
    """
    suggestions = []
    passed = True
    
    # Kiểm tra Sharpe
    if delay == 1:
        if metrics.get("Sharpe", 0) < 1.25:
            passed = False
            suggestions.append("Sharpe thấp (<1.25) cho Delay=1. Cân nhắc tăng tính ổn định của alpha (ví dụ: thêm smoothing, giảm overfitting).")
    else:  # delay == 0
        if metrics.get("Sharpe", 0) < 2.0:
            passed = False
            suggestions.append("Sharpe thấp (<2.0) cho Delay=0. Cần cải thiện lợi nhuận điều chỉnh rủi ro.")
    
    # Kiểm tra Turnover: phải nằm trong khoảng 1% - 70%
    turnover = metrics.get("Turnover", 0)
    if not (0.01 <= turnover <= 0.70):
        passed = False
        suggestions.append("Turnover không nằm trong khoảng 1%-70%. Hãy kiểm soát tần suất giao dịch để giảm chi phí.")
    
    # Kiểm tra Fitness
    if delay == 1:
        if metrics.get("Fitness", 0) < 1.0:
            passed = False
            suggestions.append("Fitness thấp (<1.0) cho Delay=1. Cần tối ưu hóa sự cân bằng giữa lợi nhuận, ổn định và chi phí giao dịch.")
    else:
        if metrics.get("Fitness", 0) < 1.3:
            passed = False
            suggestions.append("Fitness thấp (<1.3) cho Delay=0. Cần cải thiện chất lượng alpha.")
    
    # Có thể thêm kiểm tra các chỉ số khác như Drawdown, Returns, Margin nếu cần
    
    return {
        "passed": passed,
        "suggestions": suggestions,
        "metrics": metrics
    }

# Ví dụ sử dụng:
if __name__ == "__main__":
    # Giả lập kết quả của một công thức alpha
    simulated_metrics = {
        "Sharpe": 1.10,     # ví dụ: 1.10, không đạt điều kiện cho Delay=1
        "Turnover": 0.05,   # 5%, nằm trong khoảng 1%-70%
        "Fitness": 0.95,    # ví dụ: dưới ngưỡng 1.0 cho Delay=1
        "Drawdown": 3.0,    # 3%
        "Returns": 7.0,     # 7%
        "Margin": 60.0      # 60%
    }
    
    # Giả sử alpha của bạn có Delay=1
    result = evaluate_alpha_metrics(simulated_metrics, delay=1)
    if result["passed"]:
        print("Alpha đạt yêu cầu!")
    else:
        print("Alpha không đạt yêu cầu. Gợi ý điều chỉnh:")
        for s in result["suggestions"]:
            print("-", s)
    
    print("\nKết quả đánh giá:", result["metrics"])
