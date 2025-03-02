import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# ----------------------
# 1. Crawl dữ liệu từ API (Ví dụ: Alpha Vantage)
# ----------------------
def fetch_stock_data(api_key, symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data["Time Series (Daily)"]).T
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })
    df = df.astype(float)
    return df

# ----------------------
# 2. Crawl dữ liệu từ trang web động (Ví dụ: Yahoo Finance)
# ----------------------
def crawl_yahoo_finance(symbol):
    driver = webdriver.Edge()
    driver.get(f"https://finance.yahoo.com/quote/{symbol}/history")
    time.sleep(5)  # Chờ trang tải
    
    # Lấy dữ liệu bằng Selenium
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"data-test": "historical-prices"})
    df = pd.read_html(str(table))[0]
    driver.quit()
    return df

# ----------------------
# 3. Xử lý dữ liệu và tính toán chỉ số
# ----------------------
def calculate_metrics(df):
    # Tính Returns hàng ngày
    df["Returns"] = df["Close"].pct_change()
    
    # Tính Sharpe Ratio (giả sử risk-free rate = 0)
    sharpe_ratio = np.sqrt(252) * (df["Returns"].mean() / df["Returns"].std())
    
    # Tính Drawdown
    df["Cumulative"] = (1 + df["Returns"]).cumprod()
    df["Peak"] = df["Cumulative"].cummax()
    df["Drawdown"] = (df["Cumulative"] - df["Peak"]) / df["Peak"]
    max_drawdown = df["Drawdown"].min()
    
    return sharpe_ratio, max_drawdown

# ----------------------
# 4. Kiểm tra tiêu chí
# ----------------------
def check_criteria(sharpe, drawdown, turnover):
    criteria = {
        "Sharpe >= 1.25": sharpe >= 1.25,
        "Drawdown <= 5%": abs(drawdown) <= 0.05,
        "Turnover 1%-70%": 0.01 <= turnover <= 0.7
    }
    return criteria

# ----------------------
# 5. Ví dụ sử dụng
# ----------------------
if __name__ == "__main__":
    # Crawl dữ liệu
    api_key = "ZPDKNRX9MTWQXXB3"  # Thay bằng API key thực tế

    stock_code = [
        "A", "AA", "AACT", "AADI", "AAL", "AAM", "AAME", "AAMI", "AAOI", "AAON", "AAP", "AAPL", "AARD", "AB", "ABAT", "ABBV", "ABCB", "ABCL", "ABEO", "ABG", "ABL", "ABLV", "ABM", "ABNB", "ABOS", "ABP", "ABSI", "ABT", "ABTS", "ABUS", "ABVC", "ABVE", "AC", "ACA", "ACAD", "ACCD", "ACCO", "ACCS", "ACDC", "ACEL", "ACET", "ACGL", "ACHC", "ACHR", "ACHV", "ACI", "ACIC", "ACIU", "ACIW", "ACLS", "ACLX", "ACM", "AECOM", "ACMR", "ACN", "ACNB", "ACNT", "ACOG", "ACON", "ACRS", "ACRV", "ACT", "ACTG", "ACTU", "ACU", "ACVA", "ACXP", "ADBE", "ADCT", "ADD", "ADEA", "ADGM", "ADI", "ADIL", "ADM", "ADMA", "ADN", "ADNT", "ADP", "ADPT", "ADSE", "ADSK", "ADT", "ADTN", "ADTX", "ADUS", "ADV", "ADVM", "AEE", "AEHL", "AEHR", "AEI", "AEIS", "AEMD", "AENT", "AEO", "AEON", "AEP", "AER", "AERT", "AES"
    ]

    out = str()

    for symbol in stock_code:
        # Lấy dữ liệu từ Alpha Vantage
        # stock_data = fetch_stock_data(api_key, symbol)
        stock_data = crawl_yahoo_finance(symbol)
        
        # Tính toán chỉ số
        sharpe, drawdown = calculate_metrics(stock_data)
        turnover = 0.0258  # Giả định từ dữ liệu đầu vào
        
        # Kiểm tra tiêu chí
        criteria_status = check_criteria(sharpe, drawdown, turnover)
        out += "Kết quả kiểm tra tiêu chí:\n"
        for key, value in criteria_status.items():
            out += f"- {key}: {'Đạt' if value else 'Không đạt'}\n"

    f = open("report.txt", 'w')
    f.write(out)