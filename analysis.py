import requests
import json
import time
from datetime import datetime, timedelta

def run():
    try:
        # 強制刷新快取，對準 00981A
        url = f"https://www.ezmoney.com.tw/api/UnitMarketRatio/GetUnitMarketRatio?fundCode=49YTW&t={int(time.time())}"
        res = requests.get(url, timeout=15)
        data = res.json()[0]
        
        tw_time = datetime.utcnow() + timedelta(hours=8)
        
        info = {
            "update_time": tw_time.strftime("%Y-%m-%d %H:%M:%S"),
            "price": float(data.get('MarketPrice', 0)),
            "nav": float(data.get('Nav', 0)),
            "ratio": float(data.get('Ratio', 0))
        }
        
        with open('etf_data.json', 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=4)
        print("Success")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
