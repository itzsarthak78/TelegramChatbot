import os
import telebot
from openai import OpenAI
from flask import Flask, request

# Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq Client Setup
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def receive_update():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return 'Forbidden', 403

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Groq se fast reply mangwana
        completion = client.chat.completions.create(
            model="llama3-8b-8192", # Ye sabse best model hai Groq ka
            messages=[
                {"role": "system", "content": "Aapka naam Sarthak hai. Aap ek intelligent AI assistant hain."},
                {"role": "user", "content": message.text}
            ]
        )
        
        bot.reply_to(message, completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "Abhi mere dimaag mein thoda congestion hai, thodi der baad try karein!")

@app.route('/')
def home():
    return "Sarthak Groq Bot is Online!", 200
