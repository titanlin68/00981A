import requests
import json
import time
from datetime import datetime, timedelta

def get_data():
    try:
        # 強制刷新快取
        url = f"https://www.ezmoney.com.tw/api/UnitMarketRatio/GetUnitMarketRatio?fundCode=49YTW&t={int(time.time())}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        res = requests.get(url, headers=headers, timeout=15)
        data = res.json()[0]
        
        tw_time = datetime.utcnow() + timedelta(hours=8)
        
        output = {
            "update_time": tw_time.strftime("%Y-%m-%d %H:%M:%S"),
            "price": float(data.get('MarketPrice', 0)),
            "nav": float(data.get('Nav', 0)),
            "ratio": float(data.get('Ratio', 0))
        }
        
        with open('etf_data.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
        print("Success")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_data()
