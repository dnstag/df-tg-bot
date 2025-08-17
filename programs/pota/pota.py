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

import requests
import logging
from telegram import Update
from telegram.ext import Application, CallbackContext
from telegram.constants import ParseMode
from config import Config
from programs.pota import POTAAPI, Park, POTAProfile
from programs.program import Program
import util

logger = logging.getLogger(__name__)

class POTA(Program):
    def __init__(self, app: Application, config: Config):
        super().__init__(app)
        self.config = config
        self.api = POTAAPI()

        logger.debug("Initialisiere POTA Modul")
        self.register_handler("pota_profile", self._pota_profile_cmd, "Zeigt das POTA-Profil eines Benutzers an.")
        self.register_handler("pota_park", self._pota_park_cmd, "Zeigt Informationen zu einem POTA-Park an.")
        self.register_handler("pota_parks_range", self._pota_parks_range_cmd, "Zeigt Parks in der Nähe eines Grids an.")

    def get_config(self):
        return self.config

    async def _pota_profile_cmd(self, update: Update, context: CallbackContext):
        if not context.args:
            await update.message.reply_text("Bitte gib dein Rufzeichen an, z.B. /pota_profile DL1XYZ")
            return
        logger.debug("POTA Profil Befehl aufgerufen mit Rufzeichen: %s, von Benutzer: %s", context.args[0], update.message.from_user.username)
        callsign = context.args[0]

        profile = self.api.get_profile(callsign)

        await update.message.reply_text(
            f"POTA Profil für: <i>{callsign.upper()}</i>\n"
            f"\n"
            f"<b>Aktivierer:</b>\n"
            f"🗺️ Parks: {profile.activator_sucessful_parks} / {profile.activator_attempted_parks}\n"
            f"📻 Aktivierungen: {profile.activator_sucessful_activations} / {profile.activator_attempted_activations}\n"
            f"📡 QSOs: {profile.activator_sucessful_qsos} / {profile.activator_attempted_qsos}\n"
            f"\n"
            f"<b>Jäger:</b>\n"
            f"🗺️ Parks: {profile.hunter_parks}\n"
            f"📡 QSOs: {profile.hunter_qsos}\n"
            f"\n"
            f"<b>Letzte 10 Aktivitäten:</b>\n"
            f"{''.join([f"{ref.name} - {ref.description}\n" for ref in profile.references])}", parse_mode=ParseMode.HTML)

    async def _pota_park_cmd(self, update: Update, context: CallbackContext):
        if not context.args:
            await update.message.reply_text("Bitte gib die Parkreferenz an, z.B. /pota_park DE-0693")
            return

        logger.debug("POTA Park Befehl aufgerufen mit Parkreferenz: %s, von Benutzer: %s", context.args[0], update.message.from_user.username)
        park_reference = context.args[0].upper()
        park = self.api.get_park(park_reference)

        if not park:
            await update.message.reply_text(f"Fehler beim Abrufen des POTA-Parks ({park_reference})")
            return

        await update.message.reply_text(
            f"Park: <b>{park.name} - {park.description}</b>\n"
            f"Aktiv: {'Ja' if park.active else 'Nein'}\n"
            f"Grid: {park.grid6}\n"
            f"Koordinaten: {park.coordinates[0]}, {park.coordinates[1]}\n"
            # f"Region: {park.locationDesc} - {park.locationName}\n"
            f"Park-Typ: {park.park_type}\n"
            f"Erstaktivierung: {park.first_activator} am {park.first_activation_date}", parse_mode=ParseMode.HTML)

# /pota_parks_range
    async def _pota_parks_range_cmd(self, update: Update, context: CallbackContext):
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