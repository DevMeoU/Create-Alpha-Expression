import os
import pandas as pd
import requests
import time
import schedule
import sys

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

# Biến toàn cục dùng để theo dõi chỉ số mã cổ phiếu hiện tại
current_index = 0

def fetch_stock_data(symbol, start_date, end_date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?apiKey=4_xgapQxbkxlimxSVH1wUespPyEJmywz"
    response = requests.get(url)
    time.sleep(5)  # Nếu cần chờ theo tốc độ phản hồi API
    json_data = response.json()
    
    if "results" not in json_data:
        print(f"Lỗi khi lấy dữ liệu cho {symbol}:", json_data)
        return None

    data = json_data["results"]
    df = pd.DataFrame(data)
    # Chuyển đổi cột 't' từ timestamp (milliseconds) sang datetime
    df['t'] = pd.to_datetime(df['t'], unit='ms')
    df = df.rename(columns={
        "o": "Open",
        "h": "High",
        "l": "Low",
        "c": "Close",
        "v": "Volume"
    })
    df = df.sort_values(by="t")
    return df

def job():
    global current_index
    if current_index >= len(stock_codes):
        print("Đã xử lý hết các mã cổ phiếu. Thoát chương trình.")
        sys.exit(0)  # Thoát chương trình sau khi hoàn thành
    
    symbol = stock_codes[current_index]
    print(f"Đang xử lý mã: {symbol}")
    # Lấy dữ liệu từ 2024-01-01 đến 2025-01-01
    data = fetch_stock_data(symbol, "2024-01-01", "2025-01-01")
    if data is not None:
        # Ghi dữ liệu ra file Excel, thêm vào file nếu file đã tồn tại, mỗi mã được ghi vào một sheet riêng
        output_filename = "stock_data.xlsx"
        # Kiểm tra xem file đã tồn tại hay chưa
        if os.path.exists(output_filename):
            mode = 'a'
        else:
            mode = 'w'
        with pd.ExcelWriter(output_filename, mode=mode, engine="openpyxl", if_sheet_exists='replace') as writer:
            data.to_excel(writer, sheet_name=symbol, index=False)
        print(f"Dữ liệu của {symbol} đã được ghi vào file {output_filename} trong sheet {symbol}")
    else:
        print(f"Không có dữ liệu cho {symbol}")
    
    current_index += 1

def main():
    # Lên lịch gọi job() mỗi 12 giây
    schedule.every(12).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
