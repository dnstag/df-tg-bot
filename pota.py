#
# pota.py - This file is part of DF-TG-Bot
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
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from config import Config
import util

logger = logging.getLogger(__name__)

class POTA:
    def __init__(self, app: ApplicationBuilder, add_help_text: callable, config: Config):
        logger.debug("Initialisiere POTA Modul")
        app.add_handler(CommandHandler("pota_profile", self.pota_profile_cmd))
        logger.debug("Registriere /pota_profile Befehl")
        app.add_handler(CommandHandler("pota_park", self.pota_park_cmd))
        logger.debug("Registriere /pota_park Befehl") 
        app.add_handler(CommandHandler("pota_parks_range", self.pota_parks_range_cmd))
        logger.debug("Registriere /pota_parks_range Befehl")
        add_help_text("pota_profile", "Zeigt das POTA-Profil eines Benutzers an.")
        add_help_text("pota_park", "Zeigt Informationen zu einem POTA-Park an.")
        add_help_text("pota_parks_range", "Zeigt alle POTA-Parks in einem bestimmten Bereich an.")

        self.config = config

    def get_config(self):
        return self.config

# /pota_profile
    async def pota_profile_cmd(self, update: Update, context: ContextTypes):
        if not context.args:
            await update.message.reply_text("Bitte gib dein Rufzeichen an, z.B. /pota_profile DL1XYZ")
            return
        logger.debug("POTA Profil Befehl aufgerufen mit Rufzeichen: %s, von Benutzer: %s", context.args[0], update.message.from_user.username)
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
            if len(recent_activity) >= 10:  # Begrenze auf die letzten 5 Aktivitäten
                break


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
        f"<b>Letzte 10 Aktivitäten:</b>\n"
        f"{''.join(recent_activity)}", parse_mode=ParseMode.HTML)

# /pota_park
    async def pota_park_cmd(self, update: Update, context: ContextTypes):
        if not context.args:
            await update.message.reply_text("Bitte gib die Parkreferenz an, z.B. /pota_park DE-0693")
            return

        logger.debug("POTA Park Befehl aufgerufen mit Parkreferenz: %s, von Benutzer: %s", context.args[0], update.message.from_user.username)

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

        logger.debug("POTA Parks Range Befehl aufgerufen mit Grid: %s, von Benutzer: %s", context.args[0], update.message.from_user.username)

        grid = context.args[0].upper()
        lat1, lon1 = util.maidenhead_locator_to_latlon(grid)

        # Default auf 50 km setzen, wenn kein Bereich angegeben ist
        range = int(context.args[1]) if len(context.args) > 1 else int(self.config.pota_default_range)

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

        # Unterschiedliche Ausgabeformate behandeln
        if "features" in data:
            for park in data["features"]:
                dist = util.haversine_distance(lat1, lon1, park["geometry"]["coordinates"][1], park["geometry"]["coordinates"][0])
                if dist <= range:
                    parks_info.append(f"{park['properties']['reference']} - {park['properties']['name']} - {dist:.1f} km\n")
                if len(parks_info) >= self.config.pota_max_parks:  # Begrenze die Anzahl der Parks auf 25
                    break
        else:
            for park in data:
                dist = util.haversine_distance(lat1, lon1, park["latitude"], park["longitude"])
                if dist <= range:
                    parks_info.append(f"{park['reference']} - {park['name']} - {dist:.1f} km\n")
                if len(parks_info) >= self.config.pota_max_parks:  # Begrenze die Anzahl der Parks auf 25
                    break

        sorted_distances = sorted(parks_info, key=lambda x: float(x.split('-')[-1].split()[0]))
        parks_info = sorted_distances

        if len(parks_info) == 0:
            await update.message.reply_text("Keine Parks im angegebenen Bereich gefunden.")
            return
        
        await update.message.reply_text(f"Parks im Bereich von {grid} ({range}km):\n{''.join(parks_info)}", parse_mode=ParseMode.HTML)