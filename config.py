import json
import os

class Config:
    def __init__(self, filepath="config.json"):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Konfigurationsdatei nicht gefunden: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                self._data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Fehler beim Parsen der JSON-Datei: {e}")

    @property
    def token(self):
        return self._data.get("token", "")

    def as_dict(self):
        """Gibt die gesamte Konfiguration als Dictionary zurück"""
        return self._data
