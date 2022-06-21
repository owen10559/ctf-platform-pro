import json

config = dict()

def refresh():
    global config
    with open("config.json") as f:
        config = json.load(f)

refresh()