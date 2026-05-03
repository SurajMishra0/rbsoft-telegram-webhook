import os
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET', 'your-secret-key-change-this')

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.ok
    except Exception as e:
        print(f"Error: {e}")
        return False

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "RBSoft Webhook is running!"})

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400
    
    event_type = data.get('event', 'unknown')
    
    if event_type == 'message.received':
        message = f"📨 New SMS!\nFrom: {data.get('from')}\nMessage: {data.get('text')}"
    elif event_type == 'call.added':
        message = f"📞 Call!\nFrom: {data.get('from')}"
    else:
        message = f"Event: {event_type}\n{json.dumps(data, indent=2)}"
    
    send_telegram_message(message)
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)