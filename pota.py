import json
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode
import util

class POTA:
    def __init__(self, app: ApplicationBuilder):
        app.add_handler(CommandHandler("pota_profile", self.pota_profile_cmd))
        app.add_handler(CommandHandler("pota_park", self.pota_park_cmd))
        app.add_handler(CommandHandler("pota_parks_range", self.pota_parks_range_cmd))

# /pota_profile
    async def pota_profile_cmd(self, update: Update, context: ContextTypes):
        if not context.args:
            await update.message.reply_text("Bitte gib dein Rufzeichen an, z.B. /pota_profile DL1XYZ")
            return

        callsign = context.args[0]

        url = f"https://api.pota.app/profile/{callsign.upper()}"
        response = requests.get(url)

        if response.status_code != 200:
            await update.message.reply_text(f"Fehler beim Abrufen des POTA-Profils ({response.status_code})")
            return

        data = response.json()
        successful_activations = data["stats"]["activator"]["activations"]
        successful_parks = data["stats"]["activator"]["parks"]
        successful_qsos = data["stats"]["activator"]["qsos"]
        attempts_activations = data["stats"]["attempts"]["activations"]
        attempts_parks = data["stats"]["attempts"]["parks"]
        attempts_qsos = data["stats"]["attempts"]["qsos"]
        hunter_parks = data["stats"]["hunter"]["parks"]
        hunter_qsos = data["stats"]["hunter"]["qsos"]
        recent_activity = []


        for activity in data["recent_activity"]["activations"]:
            recent_activity.append(f"📅 {activity['date']} - {activity['reference']} {activity['park']} - {activity['total']} QSOs\n")


        await update.message.reply_text(
        f"POTA Profil für: <i>{callsign.upper()}</i>\n"
        f"\n"
        f"<b>Aktivierer:</b>\n"
        f"🗺️ Parks: {successful_parks} / {attempts_parks}\n"
        f"📻 Aktivierungen: {successful_activations} / {attempts_activations}\n"
        f"📡 QSOs: {successful_qsos} / {attempts_qsos}\n"
        f"\n"
        f"<b>Jäger:</b>\n"
        f"🗺️ Parks: {hunter_parks}\n"
        f"📡 QSOs: {hunter_qsos}\n"
        f"\n"
        f"<b>Letzte Aktivitäten:</b>\n"
        f"{''.join(recent_activity)}", parse_mode=ParseMode.HTML)

# /pota_park
    async def pota_park_cmd(self, update: Update, context: ContextTypes):
        if not context.args:
            await update.message.reply_text("Bitte gib die Parkreferenz an, z.B. /pota_park DE-0693")
            return

        park_reference = context.args[0].upper()

        url = f"https://api.pota.app/park/{park_reference}"
        response = requests.get(url)

        if response.status_code != 200:
            await update.message.reply_text(f"Fehler beim Abrufen des POTA-Parks ({response.status_code})")
            return

        data = response.json()

        await update.message.reply_text(
            f"Park: <b>{data['reference']} - {data['name']}</b>\n"
            f"Aktiv: {'Ja' if data['active'] else 'Nein'}\n"
            f"Grid: {data['grid6']}\n"
            f"Koordinaten: {data['latitude']}, {data['longitude']}\n"
            f"Region: {data['locationDesc']} - {data['locationName']}\n"
            f"Park-Typ: {data['parktypeDesc']}\n"
            f"Erstaktivierung: {data['firstActivator']} am {data['firstActivationDate']}", parse_mode=ParseMode.HTML)

# /pota_parks_range
    async def pota_parks_range_cmd(self, update: Update, context: ContextTypes):
        if not context.args:
            await update.message.reply_text("Bitte gib dein 6-stelliges Grid an, z.B. /pota_parks_range JN39mf")
            return

        grid = context.args[0].upper()
        lat1, lon1 = util.maidenhead_locator_to_latlon(grid)

        url = f"https://api.pota.app/park/grid/{grid}"
        response = requests.get(url)

        if response.status_code != 200:
            await update.message.reply_text(f"Fehler beim Abrufen der umgebenden Parks ({response.status_code})")
            return

        data = response.json()

        if not data:
            await update.message.reply_text("Keine Parks im angegebenen Bereich gefunden.")
            return

        parks_info = []
        for park in data["features"]:
            dist = util.haversine_distance(lat1, lon1, park["geometry"]["coordinates"][1], park["geometry"]["coordinates"][0])
            if dist <= 50:
                parks_info.append(f"{park['properties']['reference']} - {park['properties']['name']} - {dist:.1f} km\n")
            if len(parks_info) >= 25:  # Begrenze die Anzahl der Parks auf 25
                break

        sorted_distances = sorted(parks_info, key=lambda x: float(x.split('-')[-1].split()[0]))
        parks_info = sorted_distances[:25]  # Nimm nur die 25 nächsten
        await update.message.reply_text(f"Parks im Bereich von {grid} (50km):\n{''.join(parks_info)}", parse_mode=ParseMode.HTML)