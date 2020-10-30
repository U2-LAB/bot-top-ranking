import json
import os

from bot.marsh_schemas import StateSchema
from bot.work_with_csv import get_music_csv, create_csv


class State:
    def __init__(self):
        self.schema = StateSchema()
        self.filename = os.getenv("MUSIC_FILE")
        self.config_filename = (
            os.getenv("SAVED_JSON")
            if os.path.exists(os.getenv("SAVED_JSON"))
            else os.getenv("DEFAULT_JSON")
        )
        self.config = self.loads_config()

    def loads_config(self):
        with open(self.config_filename) as r_file:
            json_data = json.load(r_file)
            config = self.schema.load(json_data)

        if not config["songs"]:
            create_csv(self.filename, config["count_music"])
            config["songs"] = self.get_songs()

        config["songs"] = sorted(config["songs"], key=lambda song: song["title"])
        for idx, _ in enumerate(config["songs"]):
            config["songs"][idx]["pos"] = idx + 1  # positions of songs starts by 1
        return config

    def get_songs(self):
        return get_music_csv(self.filename)

    def save_config(self):
        with open(os.getenv("SAVED_JSON"), 'w') as w_file:
            json_data = self.schema.dump(self.config)
            json.dump(json_data, w_file, indent=4)
