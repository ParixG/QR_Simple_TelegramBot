import qrcode
from telegram import *
from telegram.ext import *
from telegram._update import *
import logging
import os

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def qr_maker(data:str):
    img = qrcode.make(data,version=4,border=2)
    type(img)
    img.save("qr.png")

def new_button(key:str):
    keyboard = [[KeyboardButton(key)]]
    return ReplyKeyboardMarkup(keyboard,resize_keyboard=True,one_time_keyboard=True)

GETQR = range(1)

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    await update.message.reply_text("🧡 Wellcome to Simple QR Code Generator bot.",reply_markup=new_button("New QR 🖼"))

async def get_data(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    await update.message.reply_text("⚙️ Send your text or link:",reply_markup=new_button("Cancel ❌"))
    return GETQR

async def get_qr(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    data = update.message.text
    qr_maker(data)
    await update.message.reply_photo("qr.png","✅ Done.",reply_markup=new_button("New QR 🖼"))
    return ConversationHandler.END

async def cancel(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    await update.message.reply_text("☑️ Canceled. See you later.\nClick \"New QR 🖼\" to start again.",reply_markup=new_button("New QR 🖼"))
    return ConversationHandler.END

if __name__ == '__main__':

    BOT_TOKEN = os.getenv("BOT_TOKEN")
    PORT = int(os.getenv("PORT", 5000))
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start",start))

    conv_handler = ConversationHandler(entry_points=[MessageHandler(filters.Regex("^New QR 🖼$"),get_data)],
        states={
            GETQR:[MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^Cancel ❌$") & ~filters.Regex("^New QR 🖼$"),get_qr)]
        },
        fallbacks=[MessageHandler(filters.Regex("^Cancel ❌$"),cancel)]
    )

    app.add_handler(conv_handler)

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
    )

