from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import os

app = Flask(__name__)
CORS(app)

stocks_list = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "TATAMOTORS.NS", "SBIN.NS", "BHARTIARTL.NS"]

@app.route('/api/scan', methods=['GET'])
def scan_market():
    scanned_data = []
    
    for symbol in stocks_list:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="5d", interval="1d")
            if not df.empty:
                cmp = round(df['Close'].iloc[-1], 2)
                
                scanned_data.append({
                    "symbol": symbol.replace(".NS", ""),
                    "ltp": cmp,
                    "tf": "HIT",
                    "zone": "Demand Zone (DBR)",
                    "trend": "Bullish (50 SMA Up)",
                    "htf": "[MIT - Monthly Demand Zone Touch]",
                    "sector": "Nifty Index"
                })
        except Exception as e:
            print(f"Error for {symbol}: {e}")
            
    return jsonify(scanned_data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
