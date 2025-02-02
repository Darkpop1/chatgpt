import openai
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

# .env file से API Keys लोड करें
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI API Key सेट करें
openai.api_key = OPENAI_API_KEY

# /start command का function
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! I am an AI-powered bot. Ask me anything!")

# OpenAI API से message process करें
async def chat_with_gpt(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text

    try:
        # OpenAI API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
        )
        reply_text = response["choices"][0]["message"]["content"]
    
    except Exception as e:
        reply_text = f"Error: {str(e)}"

    await update.message.reply_text(reply_text)

# Main function (Bot start करने के लिए)
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Commands को add करें
    app.add_handler(CommandHandler("start", start))

    # Messages को process करने के लिए
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_gpt))

    # Bot को start करें
    print("🤖 Bot is running...")
    app.run_polling()

if name == "main":
    main()
