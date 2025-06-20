from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        symbol = data['symbol']
        action = data['action']
        price = float(data['price'])
        units = 126 if action == "buy" else -126

        OANDA_API_URL = os.environ['OANDA_API_URL']  # ✅ Utilisation de ta variable ENV
        OANDA_ACCOUNT_ID = os.environ['OANDA_ACCOUNT_ID']

        url = f"{OANDA_API_URL}/accounts/{OANDA_ACCOUNT_ID}/orders"

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

        response = requests.post(url, headers=headers, json=order_data)
        response.raise_for_status()  # 🚨 Pour que Flask détecte une erreur API proprement
        return jsonify(response.json()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return "Middleware Ichimoku Karen Peloille actif!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
