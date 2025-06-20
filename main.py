app.py
from flask import Flask, request
import requests, os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    symbol = data['symbol']
    action = data['action']
    price = float(data['price'])
    units = 126 if action == "buy" else -126

    OANDA_API_URL = f"https://api-fxtrade.oanda.com/v3/accounts/{os.environ['OANDA_ACCOUNT_ID']}/orders"
    headers = {
        'Authorization': f"Bearer {os.environ['OANDA_API_KEY']}",
        'Content-Type': 'application/json'
    }

    order_data = {
        "order": {
            "units": str(units),
            "instrument": symbol,
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT",
            "stopLossOnFill": {
                "price": f"{price * (0.995 if units > 0 else 1.005):.3f}"
            }
        }
    }

    response = requests.post(OANDA_API_URL, headers=headers, json=order_data)
    return response.json(), 200

@app.route('/')
def index():
    return "Middleware Ichimoku Karen Peloille actif!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)


