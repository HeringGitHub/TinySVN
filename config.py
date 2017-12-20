import json
import os

CONFIG_PATH = "%s/.TinySVN/config.json" % os.environ['HOME']


class Config:
    def __init__(self):
        self.data = {}
        with open(CONFIG_PATH, "r") as js_file:
            try:
                self.data = json.load(js_file)
            except:
                return

    def has_proj(self, name):
        return self.data.has_key(name)

    def add_proj(self, name, path):
        if not self.has_proj(name):
            self.data[name] = {}
            self.data[name]["path"] = path
            self.data[name]["index"] = len(self.data) - 1
            self.data[name]["selected"] = 0
            self.dumps()

    def del_proj(self, name):
        if self.has_proj(name):
            idx = self.data[name]["index"]
            del self.data[name]
            for p in self.data:
                if self.data[p]["index"] > idx:
                    self.data[p]["index"] = self.data[p]["index"] - 1
            self.dumps()

    def select(self, name):
        if self.has_proj(name):
            self.data[name]["selected"] = 1
            for p in self.data:
                if p != name:
                    self.data[p]["selected"] = 0
            self.dumps()


    def dumps(self):
        with open(CONFIG_PATH, "w") as js_file:
            js_file.write(json.dumps(self.data))
