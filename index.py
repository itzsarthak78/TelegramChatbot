import os
import telebot
from openai import OpenAI
from flask import Flask, request

# 1. Environment Variables se Keys lena
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROK_API_KEY = os.getenv("GROK_API_KEY")

# 2. Bot aur OpenAI Client setup
# threaded=False zaroori hai Vercel ke liye
bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)
client = OpenAI(api_key=GROK_API_KEY, base_url="https://api.x.ai/v1")

app = Flask(__name__)

# 3. Telegram Webhook Route
@app.route('/webhook', methods=['POST'])
def receive_update():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Forbidden', 403

# 4. Sarthak Bot Logic
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Bot typing status dikhaye
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Grok API call
        completion = client.chat.completions.create(
            model="grok-beta",
            messages=[
                {"role": "system", "content": "Aapka naam Sarthak hai. Aap ek friendly aur helpful AI assistant hain."},
                {"role": "user", "content": message.text}
            ]
        )
        
        # Reply bhejna
        bot.reply_to(message, completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "Maaf kijiyega, mujhe thodi technical dikkat ho rahi hai.")

# 5. Default Route (Check karne ke liye ki bot live hai)
@app.route('/')
def index():
    return "<h1>Sarthak Bot is Running!</h1>", 200
