#
# reference.py - This file is part of DF-TG-Bot
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
from dataclasses import dataclass


@dataclass
class Reference:
    """
    Represents a reference with a name and a description.
    """
    name: str
    description: str
    coordinates: tuple[float, float]
    grid4: str
    grid6: str
    first_activator: str
    first_activation_date: str

    def __str__(self):
        return f"{self.name}: {self.description} ({self.coordinates[0]}, " \
               f"{self.coordinates[1]}) grid4: {self.grid4}, grid6: {self.grid6}, " \
               f"first activator: {self.first_activator}, first activation date: {self.first_activation_date}"

    def to_dict(self):
        """
        Converts the reference to a dictionary format.
        """
        return {
            "name": self.name,
            "description": self.description,
            "coordinates": self.coordinates,
            "grid4": self.grid4,
            "grid6": self.grid6,
            "first_activator": self.first_activator,
            "first_activation_date": self.first_activation_date
        }
    
if __name__ == "__main__":
    # Example usage
    ref = Reference(
        name="DE-0693",
        description="Biosphäre Bliesgau",
        coordinates=(48.137154, 7.576124),
        grid4="JN39",
        grid6="JN39nl",
        first_activator="DK9JC",
        first_activation_date="2015-03-08"
    )
    print(ref)
    print(ref.to_dict())