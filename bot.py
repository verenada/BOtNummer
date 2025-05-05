from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# 🔐 Встав свої ключі тут:
TELEGRAM_TOKEN = '7542699255:AAGdDN1cUlGaF950vxsOwjXgvlLeWO_yYAs'
IPQS_API_KEY = 'ZaiFOd4cutnvHHUH1yltUgVJimhhX0Lk'

# 📍 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello. Enter the number")

# 📞 Обробка повідомлення з номером
async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_number = update.message.text.strip()

    url = f"https://ipqualityscore.com/api/json/phone/{IPQS_API_KEY}/{phone_number}"
    response = requests.get(url)
    data = response.json()

    if data.get("valid"):
        result = (
            f"✅ Номер дійсний\n"
            f"🌍 Країна: {data.get('country_name', 'Невідомо')}\n"
            f"📱 Оператор: {data.get('carrier', 'Невідомо')}\n"
            f"📶 Тип лінії: {data.get('line_type', 'Невідомо')}\n"
            f"🔄 Портований: {'Так' if data.get('recent_porting') else 'Ні'}\n"
            f"🚫 Призначений для шахрайства: {'Так' if data.get('fraud_score', 0) > 85 else 'Ні'}"
        )
    else:
        result = "❌ Номер недійсний або не вдалося виконати перевірку."

    await update.message.reply_text(result)

# 🚀 Запуск бота
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone))
app.run_polling()
