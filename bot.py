import os
from google import genai
import telebot

# Kalitlarni to'g'ridan-to'g'ri muhitdan o'qiymiz
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  user_text = message.text
  try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_text,
    )
    bot.reply_to(message, response.text)
  except Exception as e:
    bot.reply_to(
        message,
        "Kechirasiz, hozir javob berishda biroz xatolik yuz berdi.",
    )


print("Bot ishga tushdi...")
bot.infinity_polling()
