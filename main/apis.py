import config
import os
import redis
import utils
import db



def get_training_info(username, training_name):
    # 根据<username>和<training_name>获取对应的main容器
    # main容器的id即为 training_id
    # 从redis中读取对应的status和ttl，其中key：<training_id>，value为该training的status，该数据的ttl即为该training的ttl
    # 返回
    ...


def create_training(username, training_name):
    # 通过 docker-compose -d -f trainings/<training_name>/docker-compose.yml -p <username>_<training_name> up 启动对应的training
    # 根据<username>和<training_name>获取对应的main容器
    # main容器的id即为 training_id
    # 将以下数据存入redis：
    # 用户拥有的training：key：<username>:trainings，value：[]，此处的value是一个列表，因此需要以类似于append的方式存入
    # training_id的status及其ttl：key：<training_id>，value：1，ttl：***，ttl具体数值从config["trainings"]["ttl"]中读取
    # 返回
    ...


def update_training_info(username, training_name):
    # 通过 docker-compose -f trainings/<training_name>/docker-compose.yml -p <username>_<training_name> COMMAND，启动或停止对应的training
    # 根据<username>和<training_name>获取对应的main容器，main容器的id即为 training_id
    # 修改其在redis中对应的status，key：<training_id>，value为对应的状态码，1表示正在运行，0表示已停止
    # 返回
    ...


def remove_training(username, training_name):
    main_container = utils.get_container(username + "_" + training_name + "_main_1")
    container_id = main_container.id
    if main_container is not None:
        os.system("docker-compose -f trainings/" + training_name + "/docker-compose.yml -p" + username + "_" + training_name + "down")
        r = redis.Redis(db.redis_conn_pool)
        pipe = r.pipeline()
        pipe.multi()
        pipe.lrem(username, 0,  training_name)
        pipe.hdel('trainging_id', container_id) 
    # pipe.delete(container_id)
        pipe.execute()  
        pipe.close()
        return "", 204
    else:
        return "", 404



def get_training_config(training_name):
    # 读取对应training的config.json文件
    # 返回
    ...


def verify_flag(training_name, flag):
    # 读取对应training的config.json文件中的flag，并返回
    # 返回
    ...

