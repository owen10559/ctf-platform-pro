import json

config = dict()

def refresh():
    """更新配置文件"""
    global config
    with open("config.json") as f:
        config = json.load(f)

# 初次加载时更新
refresh()

if __name__ == '__main__':
    print(config)