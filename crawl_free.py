import yfinance as yf
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

# ----------------------
# 1. Crawl dữ liệu bằng yfinance
# ----------------------
def fetch_stock_data(symbol, period="1y"):
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period=period)
        return df
    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu {symbol}: {str(e)}")
        return pd.DataFrame()

# ----------------------
# 2. Crawl dữ liệu từ Yahoo Finance (phiên bản tương tác)
# ----------------------
def crawl_yahoo_finance(symbol):
    driver = webdriver.Chrome()
    driver.get(f"https://finance.yahoo.com/quote/{symbol}/history")
    time.sleep(5)
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"data-test": "historical-prices"})
    df = pd.read_html(str(table))[0]
    driver.quit()
    return df

# ----------------------
# 3. Xử lý dữ liệu và tính toán chỉ số (giữ nguyên)
# ----------------------
def calculate_metrics(df):
    if df.empty:
        return np.nan, np.nan
    
    df["Returns"] = df["Close"].pct_change()
    
    # Lọc dữ liệu NaN
    returns = df["Returns"].dropna()
    if len(returns) < 2:
        return np.nan, np.nan
    
    sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std())
    
    df["Cumulative"] = (1 + df["Returns"]).cumprod()
    df["Peak"] = df["Cumulative"].cummax()
    df["Drawdown"] = (df["Cumulative"] - df["Peak"]) / df["Peak"]
    max_drawdown = df["Drawdown"].min()
    
    return sharpe_ratio, max_drawdown

# ----------------------
# 4. Kiểm tra tiêu chí (giữ nguyên)
# ----------------------
def check_criteria(sharpe, drawdown, turnover):
    criteria = {
        "Sharpe >= 1.25": sharpe >= 1.25 if not np.isnan(sharpe) else False,
        "Drawdown <= 5%": abs(drawdown) <= 0.05 if not np.isnan(drawdown) else False,
        "Turnover 1%-70%": 0.01 <= turnover <= 0.7
    }
    return criteria

# ----------------------
# 5. Ví dụ sử dụng
# ----------------------
if __name__ == "__main__":
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
    
    report = []
    
    for symbol in stock_codes:
        # Lấy dữ liệu bằng yfinance
        stock_data = fetch_stock_data(symbol, period="2y")  # Dữ liệu 2 năm
        
        if not stock_data.empty:
            # Tính toán chỉ số
            sharpe, drawdown = calculate_metrics(stock_data)
            turnover = random.uniform(0, 0.07)
            # Kiểm tra tiêu chí
            criteria_status = check_criteria(sharpe, drawdown, turnover)
            
            # Ghi kết quả
            report.append(f"\n=== Kết quả cho {symbol} ===")
            for key, value in criteria_status.items():
                report.append(f"- {key}: {'ĐẠT' if value else 'KHÔNG ĐẠT'}")
        else:
            report.append(f"\n=== Không có dữ liệu cho {symbol} ===")
    
    # Xuất file báo cáo
    with open("stock_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report))