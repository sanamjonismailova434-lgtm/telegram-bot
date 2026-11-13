import os
from google import genai
import telebot

# Kalitlarni Railway muhitidan o'qiymiz
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Gemini mijozini to'g'ri ulaymiz
client = genai.Client(api_key=GEMINI_API_KEY)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  user_text = message.text
  try:
    # To'g'ri va barqaror model nomidan foydalanamiz
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_text,
    )
    bot.reply_to(message, response.text)
  except Exception as e:
    # Xatolik nima ekanini o'zingiz ko'rishingiz uchun chatga chiqarib yuboramiz
    bot.reply_to(message, f"Xatolik yuz berdi: {str(e)}")


print("Bot ishga tushdi...")
bot.infinity_polling()
