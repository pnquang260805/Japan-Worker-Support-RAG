from telegram import Update
import httpx
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from configs.app_config import AppConfig

conf = AppConfig()
print(conf.RAG_APP_URL)
async def rag_app(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_action(ChatAction.TYPING)

    chat = update.effective_chat
    user = update.effective_user
    question = update.message.text
    payload = {
        "question": question,
        "session_id": str(chat.id)
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{conf.RAG_APP_URL}/lm/ask",
            json=payload,
            timeout=60
        )
        resp.raise_for_status()  # ném lỗi nếu status 4xx/5xx
        data = resp.json()
    await update.message.reply_text(data.get("response", "Không có phản hồi"))


app = ApplicationBuilder().token(conf.TELEGRAM_API).build()

# Mọi tin nhắn chữ (không phải lệnh) sẽ đi vào rag_app
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, rag_app))

app.run_polling()