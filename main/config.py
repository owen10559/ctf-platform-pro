import json

config = dict()

def refresh():
    """更新配置文件"""
    global config
    with open("config.json") as f:
        config = json.load(f)

# refresh()