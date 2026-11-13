import telebot
from google import genai
from google.genai import types

# Kalitlar va ID
BOT_TOKEN = "8231254487:AAEFAnPshw8EectAaBQUAoNFbKOcEPSxzz4"
GEMINI_API_KEY = "AQ.Ab8RN6KyPvuckAaBmzy4iRqw-HSVnnzY3IMSn62LavdmtA8Cog"
ADMIN_ID = 8019018007

bot = telebot.TeleBot(BOT_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

# Botning xarakteri va vazifasi
SYSTEM_PROMPT = """
Sen foydalanuvchining shaxsiy AI yordamchisisansan. 
Senga kimdir yozsa, xuddi aqlli, vazmin, madaniyatli va qisqa-lo'nda gapiradigan shaxsiy sekretardek javob ber.
Ortiqcha gapirmagin, gapni cho'zma. Hozir egang band ekanligini, xabarni unga yetkazishingni va bo'shashi bilan o'zi aloqaga chiqishini ayt. 
Agar yozgan odamning maqsadi aniq bo'lmasa, nima masala bo'yicha yozayotganini muloyimlik bilan so'rab ol.
O'zbek tilida (yoki foydalanuvchi qaysi tilda yozsa, o'sha tilda) javob ber.
"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id == ADMIN_ID:
        bot.reply_to(message, "Salom! Shaxsiy AI yordamchingiz ishga tushdi. Kim yozsa, darhol javob berib sizga xabar yuboraman.")
    else:
        bot.reply_to(message, "Assalomu alaykum! Men shaxsiy yordamchiman. Xabaringizni yozib qoldiring, darhol yetkazaman.")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.chat.id == ADMIN_ID:
        bot.reply_to(message, "Tizim ishlayapti. Boshqa odamlar yozgan xabarlar shu yerga keladi.")
        return

    user_name = message.from_user.first_name or "Noma'lum"
    username = f"@{message.from_user.username}" if message.from_user.username else "Username yo'q"
    user_text = message.text

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7
            )
        )
        ai_reply = response.text
    except Exception as e:
        ai_reply = "Assalomu alaykum! Xabaringizni qabul qildim, tez orada egamga yetkazaman."

    bot.reply_to(message, ai_reply)

    report = (
        f"📩 **Yangi xabar keldi!**\n\n"
        f"👤 **Kim:** {user_name} ({username})\n"
        f"🆔 **ID:** `{message.from_user.id}`\n"
        f"💬 **Yozgan xabari:** {user_text}\n\n"
        f"🤖 **Bot javobi:** {ai_reply}"
    )
    bot.send_message(ADMIN_ID, report, parse_mode="Markdown")

print("Bot ishga tushdi...")
bot.infinity_polling()
  
