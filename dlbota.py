import json
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode

class DLBOTA:
    def __init__(self, app: ApplicationBuilder):
         app.add_handler(CommandHandler("dlbota_profile", self.dlbota_profile_cmd))

# /dlbota_profile
    async def dlbota_profile_cmd(self, update: Update, context: ContextTypes):
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
