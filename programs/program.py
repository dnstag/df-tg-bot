#
# program.py - This file is part of DF-TG-Bot
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
from telegram.ext import Application, CommandHandler
from typing import Coroutine, Any
import logging

logger = logging.getLogger(__name__)

class Program:
    """
    Represents an amateur radio outdoor program.
    """
    def __init__(self, app: Application):
        self._name = None
        self._description = None
        self._app = app
        self._help_texts = []

    @property
    def name(self):
        """
        Returns the name of the program.
        """
        return self._name

    @name.setter
    def name(self, value: str):
        """
        Sets the name of the program.
        """
        self._name = value

    @property
    def description(self):
        """
        Returns the description of the program.
        """
        return self._description

    @description.setter
    def description(self, value: str):
        """
        Sets the description of the program.
        """
        self._description = value

    @property
    def app(self):
        """
        Returns the Telegram application instance associated with the program.
        """
        return self._app

    @app.setter
    def app(self, value: Application):
        """
        Sets the Telegram application instance associated with the program.
        """
        raise ValueError("'app' may not be overwritten. Use the constructor to set it.")

    @property
    def help_texts(self):
        """
        Returns the help texts for the program.
        """
        return self._help_texts

    @help_texts.setter
    def help_texts(self, value: list):
        """
        Sets the help texts for the program.
        """
        raise ValueError("'help_texts' may not be overwritten. Use 'add_helptext'.")

    def _add_help_text(self, command: str, description: str):
        """
        Adds a help text for a command.
        """
        self._help_texts.append(f"/{command} - {description}")
        logger.debug("Hilfetext für %s hinzugefügt: %s", command, description)

    def register_handler(self, name: str, handler, help_text: str):
        self.app.add_handler(CommandHandler(name, handler))
        logger.debug("Registriere %s Befehl", name)
        self._add_help_text(name, help_text)

    def __str__(self):
        return f"{self.name} - {self.description}"

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
        }