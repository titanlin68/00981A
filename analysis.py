import requests
import json
import time
from datetime import datetime, timedelta

def get_etf():
    try:
        # 強制刷新快取，對準 00981A (49YTW)
        ts = int(time.time())
        url = f"https://www.ezmoney.com.tw/api/UnitMarketRatio/GetUnitMarketRatio?fundCode=49YTW&t={ts}"
        res = requests.get(url, timeout=10)
        data = res.json()[0]
        
        tw = datetime.utcnow() + timedelta(hours=8)
        
        result = {
            "update_time": tw.strftime("%Y-%m-%d %H:%M:%S"),
            "price": float(data.get('MarketPrice', 0)),
            "nav": float(data.get('Nav', 0)),
            "ratio": float(data.get('Ratio', 0))
        }
        
        with open('etf_data.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print("Done")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_etf()
