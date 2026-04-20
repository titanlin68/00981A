import requests
from bs4 import BeautifulSoup
import yfinance as yf
import json
from datetime import datetime, timedelta

def get_data():
    try:
        # 1. 獲取市價 (00981A)
        ticker = yf.Ticker("00981A.TW")
        price = ticker.fast_info['last_price']
        
        # 2. 獲取預估淨值 (維持你原本的抓取邏輯)
        # 這裡示範邏輯不變
        nav = price / 1.002 # 模擬數據示範

        diff = price - nav
        ratio = (diff / nav) * 100

        # --- 修正時區開始 ---
        # GitHub 伺服器是 UTC，加上 8 小時轉為台灣時間
        tw_time = datetime.utcnow() + timedelta(hours=8)
        update_str = tw_time.strftime("%Y-%m-%d %H:%M:%S")
        # --- 修正時區結束 ---

        data = {
            "update_time": update_str,
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
