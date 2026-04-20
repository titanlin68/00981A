import requests
import json
import time
from datetime import datetime, timedelta

def get_official_data():
    try:
        # 加上隨機時間戳 t={int(time.time())}，破解統一投信官方伺服器的快取
        timestamp = int(time.time())
        url = f"https://www.ezmoney.com.tw/api/UnitMarketRatio/GetUnitMarketRatio?fundCode=49YTW&t={timestamp}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.ezmoney.com.tw/ETF/Transaction/UnitMarketRatio?fundCode=49YTW'
        }
        
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code != 200:
            raise Exception(f"API 請求失敗，狀態碼: {res.status_code}")
            
        data = res.json()
        target = data[0]
        
        current_price = float(target.get('MarketPrice', 0))
        current_nav = float(target.get('Nav', 0))
        ratio = float(target.get('Ratio', 0))

        # 取得台灣時間
        tw_time = datetime.utcnow() + timedelta(hours=8)
        update_str = tw_time.strftime("%Y-%m-%d %H:%M:%S")

        result = {
            "update_time": update_str,
            "symbol": "00981A",
            "full_name": "主動統一台股增長",
            "price": current_price,
            "nav": current_nav,
            "ratio": ratio
        }
        
        with open('etf_data.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
            
        print(f"數據同步成功！最後校準時間：{update_str}")

    except Exception as e:
        print(f"同步發生錯誤: {str(e)}")

if __name__ == "__main__":
    get_official_data()
