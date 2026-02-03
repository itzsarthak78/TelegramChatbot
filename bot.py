import os
import telebot
from openai import OpenAI

# 1. API Keys setup (Render ke dashboard se uthayega)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROK_API_KEY = os.getenv("GROK_API_KEY")

# 2. Clients initialize karein
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(
    api_key=GROK_API_KEY,
    base_url="https://api.x.ai/v1",
)

# 3. Message handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # User ko dikhe ki Sarthak soch raha hai
        bot.send_chat_action(message.chat.id, 'typing')

        # Grok AI se response lena
        completion = client.chat.completions.create(
            model="grok-beta", 
            messages=[
                {
                    "role": "system", 
                    "content": "Aapka naam Sarthak hai. Aap ek bahut hi friendly, mazakiya aur samajhdaar AI hain. Aap Hindi aur English dono mein baat kar sakte hain."
                },
                {"role": "user", "content": message.text},
            ]
        )

        # AI ka jawab nikalna
        sarthak_reply = completion.choices[0].message.content
        
        # Jawab bhejna
        bot.reply_to(message, sarthak_reply)

    except Exception as e:
        print(f"Error occurred: {e}")
        bot.reply_to(message, "Bhai, thoda network issue hai lagta hai. Sarthak abhi rest kar raha hai!")

# 4. Bot start karein
if __name__ == "__main__":
    print("Sarthak Bot is now Online...")
    bot.infinity_polling()
