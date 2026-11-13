import os
from google import genai
import telebot

# Bot tokeningiz va Gemini kalitini shu yerga yozasiz
TELEGRAM_BOT_TOKEN = "8231254487:AAEFAnPshw8EectAaBQUAoNFbKOcEPSxzz4"
GEMINI_API_KEY = "AQ.Ab8RN6KyPvuckAaBmzy4iRqw-HSVnnzY3IMSn62LavdmtA8Cog"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  user_text = message.text

  try:
    # Gemini'ga savolni yuboramiz va javob olamiz
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


# Botni ishga tushiramiz
print("Bot ishga tushdi...")
bot.infinity_polling()
