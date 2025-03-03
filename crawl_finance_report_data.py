import yfinance as yf
import pandas as pd
import os

# Danh sách mã cổ phiếu cần xử lý
stock_codes = [
    "A", "AA", "AACT", "AADI", "AAL", "AAM",
    "AAME", "AAMI", "AAOI", "AAON", "AAP", "AAPL",
    "AARD", "AB", "ABAT", "ABBV", "ABCB", "ABCL",
    "ABEO", "ABG", "ABL", "ABLV", "ABM", "ABNB",
    "ABOS", "ABP", "ABSI", "ABT", "ABTS", "ABUS",
    "ABVC", "ABVE", "AC", "ACA", "ACAD", "ACCD",
    "ACCO", "ACCS", "ACDC", "ACEL", "ACET", "ACGL",
    "ACHC", "ACHR", "ACHV", "ACI", "ACIC", "ACIU",
    "ACIW", "ACLS", "ACLX", "ACM", "AECOM", "ACMR",
    "ACN", "ACNB", "ACNT", "ACOG", "ACON", "ACRS",
    "ACRV", "ACT", "ACTG", "ACTU", "ACU", "ACVA",
    "ACXP", "ADBE", "ADCT", "ADD", "ADEA", "ADGM",
    "ADI", "ADIL", "ADM", "ADMA", "ADN", "ADNT",
    "ADP", "ADPT", "ADSE", "ADSK", "ADT", "ADTN",
    "ADTX", "ADUS", "ADV", "ADVM", "AEE", "AEHL",
    "AEHR", "AEI", "AEIS", "AEMD", "AENT", "AEO",
    "AEON", "AEP", "AER", "AERT", "AES"
]

output_filename = "fundamentals.xlsx"

# Mở Excel writer để ghi nhiều sheet
with pd.ExcelWriter(output_filename, engine="openpyxl", mode='w') as writer:
    for ticker_symbol in stock_codes:
        ticker = yf.Ticker(ticker_symbol)
        
        # Lấy báo cáo tài chính
        balance_sheet = ticker.balance_sheet    # Báo cáo cân đối kế toán
        income_statement = ticker.financials    # Báo cáo kết quả kinh doanh (Income Statement)

        # Kiểm tra dữ liệu có tồn tại hay không
        if balance_sheet.empty:
            print(f"[{ticker_symbol}] Balance Sheet data is empty. Bỏ qua.")
            continue
        if income_statement.empty:
            print(f"[{ticker_symbol}] Income Statement data is empty. Bỏ qua.")
            continue

        # Xác định ngày báo cáo gần nhất (thường là cột đầu tiên)
        most_recent_date = balance_sheet.columns[0]

        # --- Tài sản ngắn hạn (assets_curr) ---
        # Trong ảnh, "Working Capital" xuất hiện. Tạm dùng "Working Capital" làm tài sản ngắn hạn.
        # Nếu muốn dùng "Total Current Assets" thì kiểm tra "Total Current Assets" thay vì "Working Capital".
        if "Total Current Assets" in balance_sheet.index:
            assets_curr_series = balance_sheet.loc["Working Capital"]
        else:
            print(f"[{ticker_symbol}] Không tìm thấy 'Total Current Assets' trong Balance Sheet.")
            if "Working Capital" in balance_sheet.index:
                print(f"[{ticker_symbol}] Sử dụng 'Working Capital' thay 'Total Current Assets' trong Balance Sheet.")
                assets_curr_series = balance_sheet.loc["Total Current Assets"]
            else:
                print(f"[{ticker_symbol}] Không tìm thấy 'Working Capital' trong Balance Sheet.")
                assets_curr_series = None

        # --- Vốn chủ sở hữu (equity) ---
        # Trong ảnh, có "Total Equity Gross Minority Interest" hoặc "Common Stock Equity".
        # Ưu tiên "Total Equity Gross Minority Interest", nếu không có thì dùng "Common Stock Equity".
        if "Total Equity Gross Minority Interest" in balance_sheet.index:
            equity_series = balance_sheet.loc["Total Equity Gross Minority Interest"]
        elif "Common Stock Equity" in balance_sheet.index:
            equity_series = balance_sheet.loc["Common Stock Equity"]
        else:
            print(f"[{ticker_symbol}] Không tìm thấy 'Total Equity' trong Balance Sheet.")
            equity_series = None

        # --- Doanh thu (sales_value) ---
        # Lấy "Total Revenue" từ Income Statement
        if "Total Revenue" in income_statement.index:
            sales_series = income_statement.loc["Total Revenue"]
        else:
            print(f"[{ticker_symbol}] Không tìm thấy 'Total Revenue' trong Income Statement.")
            sales_series = None

        # Kiểm tra nếu cả 3 mục đều None thì bỏ qua
        if (assets_curr_series is None 
            and equity_series is None 
            and sales_series is None):
            print(f"[{ticker_symbol}] Không có dữ liệu (assets_curr, equity, sales). Bỏ qua.")
            continue

        # Tạo DataFrame chứa các giá trị trên cho ngày báo cáo gần nhất
        fundamental_data = pd.DataFrame({
            "assets_curr": [
                assets_curr_series[most_recent_date] if assets_curr_series is not None else None
            ],
            "equity": [
                equity_series[most_recent_date] if equity_series is not None else None
            ],
            "sales_value": [
                sales_series[most_recent_date] if sales_series is not None else None
            ]
        }, index=[most_recent_date])

        # Ghi dữ liệu vào sheet có tên là ticker_symbol
        fundamental_data.to_excel(writer, sheet_name=ticker_symbol, index_label="Report Date")
        print(f"[{ticker_symbol}] Đã lưu dữ liệu tài chính vào sheet {ticker_symbol}.")

print(f"\nĐã hoàn thành lưu dữ liệu tài chính vào file '{output_filename}'.")
