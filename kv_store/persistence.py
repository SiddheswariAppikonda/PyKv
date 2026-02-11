import json
import os


class Persistence:
    def __init__(self, filename="data.log"):
        self.filename = filename
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.filepath = os.path.join(base_dir, "..", self.filename)

        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            open(self.filepath, "w").close()

    def write(self, key, value):
        entry = {"action": "set", "key": key, "value": value}
        with open(self.filepath, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def write_delete(self, key):
        entry = {"action": "delete", "key": key}
        with open(self.filepath, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def load(self):
        data = {}
        with open(self.filepath, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if entry.get("action") == "delete":
                        data.pop(entry["key"], None)
                    else:
                        data[entry["key"]] = entry["value"]
                except:
                    continue
        return data

    def compact(self):
        latest_data = self.load()
        with open(self.filepath, "w") as f:
            for key, value in latest_data.items():
                entry = {"action": "set", "key": key, "value": value}
                f.write(json.dumps(entry) + "\n")
