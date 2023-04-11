import os
import json


class Localizer:
    def __init__(self):
        self.guild_id: int = 0

        self.dictionary: dict[int, dict[str, dict[str, str]]] = {}
        self.load_localizations()

    def load_localizations(self):
        for server in os.listdir("dictionary"):
            with open(f"dictionary/{server}", "r", encoding="utf-8") as file:
                backward = {x: y.title() for x, y in json.loads(file.read()).items()}
                forward = {y: x for x, y in backward.items()}

            self.dictionary[int(os.path.splitext(server)[0])] = {
                "fw": forward,      # from discord name to local name
                "bw": backward      # from local name to discord name
            }

    def fw(self, name: str):
        return self.dictionary[self.guild_id]["fw"].get(name)

    def bw(self, name: str):
        return self.dictionary[self.guild_id]["bw"].get(name)


