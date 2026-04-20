import requests
import json
import time
from datetime import datetime, timedelta

def run():
    try:
        # 強制刷新快取，抓取統一投信最新數據
        ts = int(time.time())
        url = f"https://www.ezmoney.com.tw/api/UnitMarketRatio/GetUnitMarketRatio?fundCode=49YTW&t={ts}"
        
        res = requests.get(url, timeout=15)
        data = res.json()[0]
        
        # 轉為台灣時間
        tw = datetime.utcnow() + timedelta(hours=8)
        
        info = {
            "update_time": tw.strftime("%Y-%m-%d %H:%M:%S"),
            "price": float(data.get('MarketPrice', 0)),
            "nav": float(data.get('Nav', 0)),
            "ratio": float(data.get('Ratio', 0))
        }
        
        with open('etf_data.json', 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=4)
        print("Update Success")
    except Exception as e:
        print(f"Update Failed: {e}")

if __name__ == "__main__":
    run()
