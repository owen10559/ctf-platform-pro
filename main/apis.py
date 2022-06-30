import config

def get_training_info(username, training_name):
    ...

def create_training(username, training_name):
    """
    docker-compose up -f trainings/<training_name>/docker-compose.yml -p <username>_<training_name> -d
    """

    ...

def update_training_info(username, training_name):
    ...

def remove_training(username, training_name):
    """删除某个training，删除对应的容器即可"""
    ...

def get_training_config(training_name):
    ...

def verify_flag(training_name, flag):
    """验证flag是否正确"""
    ...
