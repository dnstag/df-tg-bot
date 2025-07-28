import asyncio
import nest_asyncio
import os
from telegram.ext import ApplicationBuilder, CommandHandler
from config import Config
from pota import POTA
from dlbota import DLBOTA

nest_asyncio.apply()  # Nest AsyncIO für Kompatibilität mit Render

cfg = Config(None)  # Hier wird None übergeben, um die Konfiguration nicht zu laden
# Wenn du eine Konfigurationsdatei laden möchtest, ersetze None durch den Pfad
# z.B. Config("config.json")

help_texts = []

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")

if not BOT_TOKEN or not API_URL:
    raise ValueError("BOT_TOKEN oder API_URL ist nicht gesetzt! Bitte als Umgebungsvariable setzen.")


def add_help_text(command, description):
    help_texts.append(f"/{command} - {description}")

async def main():
    # app = ApplicationBuilder().token(cfg.token).build()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    pota = POTA(app, add_help_text, cfg)
    dlbota = DLBOTA(app, add_help_text)
    app.add_handler(CommandHandler("help", lambda update, context: update.message.reply_text("\n".join(help_texts))))
    app.add_handler(CommandHandler("start", lambda update, context: update.message.reply_text("Willkommen! Benutze /help für eine Liste der Befehle.")))
      # Starte den Webhook-Server
    await app.run_webhook(
        listen="0.0.0.0",
        port=10000,  # Render erwartet standardmäßig Port 10000
        webhook_url=API_URL,
    )

if __name__ == "__main__":
    asyncio.run(main())