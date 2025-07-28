#
# config.py - This file is part of DF-TG-Bot
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

class Config:
    def __init__(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                self._data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Fehler beim Parsen der JSON-Datei: {e}")
            except FileNotFoundError:
                raise ValueError(f"Konfigurationsdatei '{filepath}' nicht gefunden.")

    @property
    def admin_id(self):
        return self._data.get("admin_id", 0)
    
    @property
    def pota_max_parks(self):
        return self._data.get("pota_max_parks", 25)
    
    @property
    def pota_default_range(self):
        return self._data.get("pota_default_range", 50)

    @property
    def webhook_url(self):
        return self._data.get("webhook_url", "")
    
    def as_dict(self):
        """Gibt die gesamte Konfiguration als Dictionary zurück"""
        return self._data
