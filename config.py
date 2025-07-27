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
    def token(self):
        return self._data.get("token", "")
    
    @property
    def admin_id(self):
        return self._data.get("admin_id", 0)
    
    @property
    def pota_max_parks(self):
        return self._data.get("pota_max_parks", 25)
    
    @property
    def pota_default_range(self):
        return self._data.get("pota_default_range", 50)

    def as_dict(self):
        """Gibt die gesamte Konfiguration als Dictionary zurück"""
        return self._data
