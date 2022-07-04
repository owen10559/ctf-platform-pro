import json
import config
import os
from urllib.parse import unquote

def get_training_info(username, training_name):
    # 根据<username>和<training_name>获取对应的main容器
    # main容器的id即为 training_id
    # 从redis中读取对应的status和ttl，其中key：<training_id>，value为该training的status，该数据的ttl即为该training的ttl
    # 返回
    ...

def create_training(username, training_name):
    # 通过 docker-compose up -d -f trainings/<training_name>/docker-compose.yml -p <username>_<training_name> 启动对应的training
    # 根据<username>和<training_name>获取对应的main容器
    # main容器的id即为 training_id
    # 将以下数据存入redis：
    # 用户拥有的training：key：<username>:trainings，value：[]，此处的value是一个列表，因此需要以类似于append的方式存入
    # training_id的status及其ttl：key：<training_id>，value：1，ttl：***，ttl具体数值从config["trainings"]["ttl"]中读取
    # 返回
    ...

def update_training_info(username, training_name):
    # 通过 docker-compose *** -d -f trainings/<training_name>/docker-compose.yml -p <username>_<training_name>，启动或停止对应的training
    # 根据<username>和<training_name>获取对应的main容器，main容器的id即为 training_id
    # 修改其在redis中对应的status，key：<training_id>，value为对应的状态码，1表示正在运行，0表示已停止
    # 返回
    ...

def remove_training(username, training_name):
    # 根据<username>和<training_name>获取对应的main容器，main容器的id即为 training_id
    # 通过docker-compose down -d -f trainings/<training_name>/docker-compose.yml -p <username>_<training_name>移除对应的training
    # 删除其在redis中的记录：
    # 用户拥有的training：key：<username>:trainings，value：[]，此处的values是一个列表，因此需要以类似于remove的方式删除
    # training_id的status及其ttl：key：<training_id>，删除此条记录
    # 返回
    ...

def get_training_config(training_name):
    # 读取对应training的config.json文件
    # 返回
    ...

def verify_flag(training_name, flag):
    # 读取对应training的config.json文件中的flag，并返回
    # url中的某些特殊符号需要解码，所以调用unquote方法进行解码
    # 由于未明确返回数据格式，所以暂时返回true和false
    
    de_flag=unquote(flag)
    de_training_name=unquote(training_name)
    # 如果目录不存在就返回false
    if not os.path.exists("../trainings/" + de_training_name):
        return "False"

    with open("../trainings/" + de_training_name + "/config.json", "r") as f:
        std_read = json.load(f)
    # flag不正确就返回false
    if (de_flag != std_read["training"]["flag"]):
        return "False"
    # flag正确就返回true
    return "True"
    # 返回
