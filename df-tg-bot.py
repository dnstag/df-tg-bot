import asyncio
import os
from telegram.ext import ApplicationBuilder, CommandHandler
from config import Config
from pota import POTA
from dlbota import DLBOTA

cfg = Config(None)  # Hier wird None übergeben, um die Konfiguration nicht zu laden
# Wenn du eine Konfigurationsdatei laden möchtest, ersetze None durch den Pfad
# z.B. Config("config.json")

help_texts = []

WEBHOOK_PATH = "/webhook"
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN ist nicht gesetzt! Bitte als Umgebungsvariable setzen.")


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
        webhook_path=WEBHOOK_PATH,
        webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}",
        # allowed_updates=None  # optional, um alle Updates zu erlauben
    )

if __name__ == "__main__":
    asyncio.run(main())