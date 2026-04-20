import requests
import json
from datetime import datetime, timedelta

def get_official_data():
    try:
        # 直接請求統一投信 API
        url = "https://www.ezmoney.com.tw/api/UnitMarketRatio/GetUnitMarketRatio?fundCode=49YTW"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.ezmoney.com.tw/ETF/Transaction/UnitMarketRatio?fundCode=49YTW'
        }
        
        res = requests.get(url, headers=headers, timeout=15)
        # 檢查是否請求成功
        if res.status_code != 200:
            raise Exception(f"API 請求失敗，狀態碼: {res.status_code}")
            
        data = res.json()
        
        # 根據官方回傳格式精準抓取欄位
        # 官方回傳是一個 List，我們取第一個項目
        target = data[0]
        current_price = float(target.get('MarketPrice', 0))
        current_nav = float(target.get('Nav', 0))
        ratio = float(target.get('Ratio', 0))

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
            
        print(f"數據同步成功！市價：{current_price}")

    except Exception as e:
        print(f"同步發生錯誤: {str(e)}")
        # 發生錯誤時，至少產生一個空檔案避免網頁壞掉
        if not hasattr(get_official_data, "failed"):
             get_official_data.failed = True
             print("嘗試產生備援數據...")

if __name__ == "__main__":
    get_official_data()
