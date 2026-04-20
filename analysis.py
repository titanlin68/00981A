import requests
import json
import time
from datetime import datetime, timedelta

def get_data():
    try:
        # 對準 00981A (49YTW) 並加入時間戳避開快取
        url = f"https://www.ezmoney.com.tw/api/UnitMarketRatio/GetUnitMarketRatio?fundCode=49YTW&t={int(time.time())}"
        res = requests.get(url, timeout=10)
        data = res.json()[0]
        
        # 轉換為台灣時間
        tw = datetime.utcnow() + timedelta(hours=8)
        
        result = {
            "update_time": tw.strftime("%Y-%m-%d %H:%M:%S"),
            "price": float(data.get('MarketPrice', 0)),
            "nav": float(data.get('Nav', 0)),
            "ratio": float(data.get('Ratio', 0))
        }
        
        with open('etf_data.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_data()
