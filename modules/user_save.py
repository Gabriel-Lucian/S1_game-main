"""For saving the user settings and progress"""
import json


class UserSave:
    def __init__(self, username):
        self.username = username
        self.lvl_info = {}

    def add_score(self, lvl_name, score):
        if lvl_name in self.lvl_info.keys():
            self.lvl_info[lvl_name].append(score)
        else:
            self.lvl_info[lvl_name] = [score]

    def try_load(self):
        try:
            self.load()
        except FileNotFoundError:
            pass

    def load(self):
        with open(f"saves/{self.username}.json", "r") as openfile:
            json_data = json.load(openfile)

        self.lvl_info = json_data

    def save(self):
        json_data = json.dumps(self.lvl_info)

        with open(f"saves/{self.username}.json", "w") as outfile:
            outfile.write(json_data)
