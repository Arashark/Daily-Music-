import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, CallbackQueryHandler, filters
import yt_dlp

BOT_TOKEN = "8041668880:AAFPw3zYkMMxAMAd_I3NBKe6Kx_J_q8_-ho"

logging.basicConfig(level=logging.INFO)

# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("فارسی", callback_data="lang_fa")],
        [InlineKeyboardButton("English", callback_data="lang_en")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("زبان خود را انتخاب کنید\nChoose your language:", reply_markup=reply_markup)

# انتخاب زبان
async def lang_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data
    if lang == "lang_fa":
        context.user_data["lang"] = "fa"
        await query.edit_message_text("نام آهنگ را وارد کن:")
    else:
        context.user_data["lang"] = "en"
        await query.edit_message_text("Send song name to search:")

# جستجو آهنگ
async def search_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    lang = context.user_data.get("lang", "en")
    await update.message.reply_text("در حال جستجو..." if lang == "fa" else "Searching...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)['entries'][0]
            url = info['webpage_url']
            title = info['title']
            await update.message.reply_text(f"آهنگ پیدا شد:\n{title}\n{url}" if lang == "fa" else f"Found:\n{title}\n{url}")
        except Exception as e:
            await update.message.reply_text("مشکلی پیش آمد!" if lang == "fa" else "Error!")

# اجرای برنامه
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(lang_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_song))

app.run_polling()
