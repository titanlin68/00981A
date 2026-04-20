import requests
from bs4 import BeautifulSoup
import yfinance as yf
import json
import os
from datetime import datetime

def get_data():
    try:
        # 1. 獲取市價 (00981A)
        ticker = yf.Ticker("00981A.TW")
        price = ticker.fast_info['last_price']
        
        # 2. 獲取預估淨值 (假設從財經網站抓取，此處以模擬邏輯示範)
        # 實務上請替換為凱基官網或玩股網的爬蟲邏輯
        url = "https://www.wantgoo.com/stock/etf/00981A/discount-premium"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        # 這裡需根據實際 HTML 標籤解析，暫以 price 代替 demo
        nav = price * 0.998  # 模擬折價 0.2%

        diff = price - nav
        ratio = (diff / nav) * 100

        data = {
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": "00981A",
            "price": round(price, 2),
            "nav": round(nav, 2),
            "ratio": round(ratio, 2),
            "status": "溢價" if ratio > 0 else "折價"
        }
        
        with open('etf_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_data()
