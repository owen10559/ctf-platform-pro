import config

def start(username, training_name):
    """
    docker-compose up -f trainings/<training_name>/docker-compose.yml -p <username>/<training_name> -d
    """
    ...

def stop(username, training_name):
    """停止某个容器"""
    ...

def remove(username, training_name):
    """删除某个training，删除对应的容器即可"""
    ...

def verify(training_name, flag):
    """验证flag是否正确"""
    ...
