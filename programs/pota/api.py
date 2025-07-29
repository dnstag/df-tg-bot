#
# api.py - This file is part of DF-TG-Bot
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

import logging
import requests
from programs.pota.park import Park
from programs.pota.profile import POTAProfile

logger = logging.getLogger(__name__)

class POTAAPI:
    def __init__(self, base_url: str = "https://api.pota.app"):
        """Initialize the API client with a base URL."""
        self.base_url = base_url

    def get_park(self, park_reference: str) -> Park:
        """Fetch details of a specific park by its reference."""
        url = f"{self.base_url}/park/{park_reference}"
        logger.debug(f"Fetching park data from {url} for reference {park_reference}")
        response = requests.get(url)

        if response.status_code != 200:
            err = f"Error fetching park data: {response.status_code} - {response.text}"
            logger.error(err)
            raise Exception(err)
        data = response.json()

        return Park(data['reference'], data['name'], (data['latitude'], data['longitude']), bool(data['active']))

    def get_profile(self, callsign: str) -> POTAProfile:
        """Fetch the profile of a specific callsign."""
        url = f"{self.base_url}/profile/{callsign}"
        logger.debug(f"Fetching profile data from {url} for callsign {callsign}")
        response = requests.get(url)

        if response.status_code != 200:
            err = f"Error fetching profile data: {response.status_code} - {response.text}"
            logger.error(err)
            raise Exception(err)
        data = response.json()

    # fetching references first
        references: list[Park] = []
        for activation in data['recent_activity']['activations']:
            references.append(Park(activation['reference'], activation['park'], (0.0, 0.0), True))

        return POTAProfile(
            data['callsign'],
            references,
            data['stats']['activator']['parks'],
            data['stats']['activator']['activations'],
            data['stats']['activator']['qsos'],
            data['stats']['attempts']['parks'],
            data['stats']['attempts']['activations'],
            data['stats']['attempts']['qsos'],
            data['stats']['hunter']['parks'],
            data['stats']['hunter']['qsos'])

if __name__ == "__main__":
    # Example usage
    api = POTAAPI()
    try:
        park = api.get_park("DE-0693")
        profile = api.get_profile("DK8YS")
        print(park)
        print(profile)
    except Exception as e:
        print(f"Failed to fetch park: {e}")
