import config

def get_training(username, training_name):
    """
    docker-compose up -f trainings/<training_name>/docker-compose.yml -p <username>_<training_name> -d
    """

    ...

def get_training_info(training_name):
    ...

def get_running_training_info(training_id):
    ...

def stop_training(training_id):
    """停止某个容器"""
    ...

def remove_training(username, training_name):
    """删除某个training，删除对应的容器即可"""
    ...

def verify_flag(training_name, flag):
    """验证flag是否正确"""
    ...
