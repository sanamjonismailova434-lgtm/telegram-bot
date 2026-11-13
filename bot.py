from google import genai
import telebot

# Token va kalitni to'g'ridan-to'g'ri shu yerga yozamiz
TELEGRAM_BOT_TOKEN = "8231254487:AAGzYNTyeMibMW7hccIxFxK-qKMQPuPQkWg"
GEMINI_API_KEY = "AQ.Ab8RN6KbyinUef1typiDr7QMHh2X9zGVUr9egrM3-01_kFTTvQ"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

# Botning xarakteri va suhbatdosh sifatidagi qoidalari
SYSTEM_INSTRUCTION = (
    "Sen juda xushmuomala, vazmin, aqlli va har qanday mavzuda "
    "mazmunli suhbat qura oladigan sirdosh do'stsan. Odamlarga har doim "
    "samimiy hurmat bilan muomala qilasan, ularning dardini tinglayverasan "
    "va har qanday vaziyatda qo'llab-quvvatlashga tayyorsan. "
    "Javoblaringni doim o'zbek tilida, iliq va tushunarli matnda yoz."
)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  user_text = message.text

  # Foydalanuvchiga bot o'ylayotganini bildirish uchun "yozmoqda..." holatini yoqamiz
  bot.send_chat_action(message.chat.id, "typing")

  try:
    # Gemini'ga xarakter va foydalanuvchi xabarini birga yuboramiz
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_text,
        config={
            "system_instruction": SYSTEM_INSTRUCTION,
            "temperature": 0.7,  # Suhbatni jonli va qiziqarli chiqishi uchun
        },
    )

    # Javobni yuboramiz
    bot.reply_to(message, response.text)

  except Exception as e:
    # Agar internet yoki API'da kichik uzilish bo'lsa, xushmuomalalik bilan bildiramiz
    bot.reply_to(
        message,
        "Uzur, biroz chalg'ib qolibman. Savolingizni qaytadan yuboring-chi,"
        " albatta suhbatni davom ettiramiz.",
    )


print("Draken bot muvaffaqiyatli ishga tushdi va suhbatga tayyor...")
bot.infinity_polling()
