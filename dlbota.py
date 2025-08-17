#
# dlbota.py - This file is part of DF-TG-Bot
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

import json
import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext
from telegram.constants import ParseMode

class DLBOTA:
    def __init__(self, app: Application, add_help_text: callable):
         app.add_handler(CommandHandler("dlbota_profile", self.dlbota_profile_cmd))
         add_help_text("dlbota_profile", "Zeigt das DLBOTA-Profil eines Benutzers an.")

# /dlbota_profile
    async def dlbota_profile_cmd(self, update: Update, context: CallbackContext):
        if not context.args:
            await update.message.reply_text("Bitte gib dein Rufzeichen an, z.B. /dlbota_profile DL1XYZ")
            return

        callsign = context.args[0]

        url = f"https://logs.dlbota.de/api/stats.php?callsign={callsign.upper()}"
        response = requests.get(url)

        if response.status_code != 200:
            await update.message.reply_text(f"Fehler beim Abrufen des DLBOTA-Profils ({response.status_code})")
            return

        data = response.json()

        if data["callsign"] != callsign.upper():
            await update.message.reply_text(f"Rufzeichen <i>{callsign.upper()}</i> nicht gefunden.", parse_mode=ParseMode.HTML)
            return

        activator_activations = data["activator"]["activations"]
        activator_bunkers = data["activator"]["bunkers"]
        activator_qsos = data["activator"]["qsos"]
        hunter_bunkers = data["hunter"]["bunkers"]
        hunter_qsos = data["hunter"]["qsos"]

        await update.message.reply_text(
        f"DLBOTA Profil für: <i>{callsign.upper()}</i>\n"
        f"\n"
        f"<b>Aktivierer:</b>\n"
        f"🗺️ Bunker: {activator_bunkers}\n"
        f"📻 Aktivierungen: {activator_activations}\n"
        f"📡 QSOs: {activator_qsos}\n"
        f"\n"
        f"<b>Jäger:</b>\n"
        f"🗺️ Bunker: {hunter_bunkers}\n"
        f"📡 QSOs: {hunter_qsos}", parse_mode=ParseMode.HTML)
