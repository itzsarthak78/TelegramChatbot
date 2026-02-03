import os
import telebot
from openai import OpenAI
from flask import Flask # Ye line add karein

# Flask setup taaki Render ko "Web" signal mile
app = Flask(__name__)

@app.route('/')
def index():
    return "Sarthak is running!"

# Baki purana code...
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROK_API_KEY = os.getenv("GROK_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
# ... (aapka baki handle_message code) ...

if __name__ == "__main__":
    # Bot ko background mein start karein
    import threading
    threading.Thread(target=bot.infinity_polling).start()
    
    # Render ka port handle karein
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
