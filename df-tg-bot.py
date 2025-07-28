#
# df-tg-bot.py - This file is part of DF-TG-Bot
# 
# Copyright (c) 2025 Yannick Seibert. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
from telegram.ext import ApplicationBuilder, CommandHandler
from config import Config
from pota import POTA
from dlbota import DLBOTA

help_texts = []
VERSION = "0.0.1-prealpha"

def parse_argv():
    parser = argparse.ArgumentParser(
        description="Draussenfunker Telegram Bot - Befehlsübersicht."
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
        help="Zeigt die Versionsnummer an und beendet das Programm."
    )

    parser.add_argument(
        "-c", "--config",
        default="config.json",
        help="Pfad zur Konfigurationsdatei (Standard: config.json)"
    )

    parser.add_argument(
        "-d", "--development",
        action="store_true",
        default=False,
        help="Führt den Bot im Entwicklungsmodus aus, d.h. Polling anstelle von Webhooks.",
    )
    parser.add_argument(
        "token",
        help="Telegram Bot Token (von BotFather erhalten)"
    )

    return parser.parse_args()    

def add_help_text(command, description):
    help_texts.append(f"/{command} - {description}")

def start(config_path, token, development):
    cfg = Config(config_path)
    app = ApplicationBuilder().token(token).build()
    pota = POTA(app, add_help_text, cfg)
    dlbota = DLBOTA(app, add_help_text)
    app.add_handler(CommandHandler("help", lambda update, context: update.message.reply_text("\n".join(help_texts))))
    app.add_handler(CommandHandler("start", lambda update, context: update.message.reply_text("Willkommen! Benutze /help für eine Liste der Befehle.")))

    if development:
        print("Starte Bot im Entwicklungsmodus (Polling)...")
        app.run_polling()
    else:
        print("Starte Bot im Produktionsmodus (Webhook)...")
        app.run_webhook(
            listen="0.0.0.0",
            port=10000,  # Render erwartet standardmäßig Port 10000
            webhook_url=cfg.webhook_url)

if __name__ == "__main__":
    args = parse_argv()
    start(args.config, args.token, args.development)