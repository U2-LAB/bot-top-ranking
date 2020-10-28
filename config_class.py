import json
import os

from work_music import get_music_csv, create_csv


class State:
    def __init__(self):
        self.filename = os.getenv("MUSIC_FILE")
        self.config_filename = (
            os.getenv("SAVED_JSON")
            if os.path.exists(os.getenv("SAVED_JSON"))
            else os.getenv("DEFAULT_JSON")
        )
        self.config = self.loads_config()

    def loads_config(self):
        with open(self.config_filename) as r_file:
            config = json.load(r_file)
        if not config["songs"]:
            create_csv(self.filename, config["countMusic"])
            config["songs"] = self.get_songs()

        config["songs"] = sorted(config["songs"], key=lambda song: song["title"])
        for idx, _ in enumerate(config["songs"]):
            config["songs"][idx]["pos"] = idx + 1  # positions of songs starts by 1
        return config

    def get_songs(self):
        return get_music_csv(self.filename)

    def save_config(self):
        data = json.load(open(self.config_filename))
        with open(os.getenv("SAVED_JSON"), 'w') as w_file:
            data["chatId"] = self.config["chatId"]
            data["usersForPromoting"] = self.config["usersForPromoting"]
            data["songs"] = self.config["songs"]
            data["pollStarted"] = self.config["pollStarted"]
            data["uploadFlag"] = self.config["uploadFlag"]
            json.dump(data, w_file, indent=4)
