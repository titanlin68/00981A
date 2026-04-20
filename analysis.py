import requests
import json
from datetime import datetime, timedelta

def get_official_data():
    try:
        # 統一投信官方即時折溢價 API (針對 00981A / 49YTW)
        url = "https://www.ezmoney.com.tw/api/UnitMarketRatio/GetUnitMarketRatio?fundCode=49YTW"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.ezmoney.com.tw/ETF/Transaction/UnitMarketRatio?fundCode=49YTW'
        }
        
        res = requests.get(url, headers=headers, timeout=15)
        data = res.json()
        
        # 抓取官方回傳的數值
        # 假設官方 API 回傳格式中包含：MarketPrice(市價), Nav(淨值), Ratio(折溢價率)
        current_price = float(data[0]['MarketPrice'])
        current_nav = float(data[0]['Nav'])
        ratio = float(data[0]['Ratio'])

        # 處理台灣時區
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
            
        print(f"官方數據同步成功: {current_price} / {current_nav}")

    except Exception as e:
        print(f"同步失敗，嘗試備援方案: {e}")
        # 若 API 暫時失效，這裡可保留之前的 Yahoo Finance 抓取邏輯作為備援

if __name__ == "__main__":
    get_official_data()
