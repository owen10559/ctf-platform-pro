import json
import config
import os
import redis
import containers
import docker
import flask
from urllib.parse import unquote
import db

app = flask.Flask(__name__)





client = docker.from_env()

@app.route("/test")
def test():
    return "ok"

@app.route("/<username>/<training_name>", methods=["get"])
def get_training_info(username, training_name):
    # Author: LRL
    # 根据<username>和<training_name>获取对应的main容器
    username = unquote(username)
    training_name = unquote(training_name)
    r = redis.Redis(db.redis_conn_pool)

    if r.exists(username) == 0:
        return "", 404
    ok = 0
    for name in r.lrange(username, 0, -1):
        if name == training_name:
            ok = 1
            break
    if ok == 0:
        return "", 404
    # main容器的id即为 training_id
    training_id = 0
    for container in client.containers.list(all=True):
        if container.name == username + "_" + training_name + "_main_1":
            training_id = container.id
            break
    # 从redis中读取对应的status和ttl，其中key：<training_id>，value为该training的status，该数据的ttl即为该training的ttl
    # 返回
    if r.exists(training_id):
        return {"training_id": training_id, "status": r.lrange(training_id, 0, 0)[0], "ttl": r.ttl(training_id)}, 200
    else:
        return {"training_id": training_id, "status": 0, "ttl": 0}, 200

@app.route("/<username>/<training_name>", methods=["post"])
def create_training(username, training_name):
    # Author: LRL
    username = unquote(username)
    training_name = unquote(training_name)
    if not os.path.exists("./trainings/" + training_name):
        return "", 404
    # 通过 docker-compose -f trainings/<training_name>/docker-compose.yml -p <username>_<training_name> up -d 启动对应的training
    cmd = "docker-compose -f ./trainings/" + training_name + "/docker-compose.yml -p " + username + "_" + training_name + " up -d"
    os.system(cmd)
    # 根据<username>和<training_name>获取对应的main容器
    container = utils.get_container(username + "_" + training_name + "_main_1")
    # main容器的id即为 training_id
    container_id = container.id
    # 将以下数据存入redis：
    # 用户拥有的training：key：<username>:trainings，value：[]，此处的value是一个列表，因此需要以类似于append的方式存入
    ttl = config.config["trainings"]["ttl"]
    r = redis.Redis(db.redis_conn_pool)
    if r.exists(container_id):
        return {"training_id": container_id, "status": r.lrange(container_id, 0, 0)[0], "ttl": r.ttl(container_id)}, 201
    r.rpush(username, training_name)
    # training_id的status及其ttl：key：<training_id>，value：1，ttl：***，ttl具体数值从config["trainings"]["ttl"]中读取
    r.rpush(container_id, 1)
    r.expire(container_id, ttl)
    # 返回
    return {"training_id": container_id, "status": r.lrange(container_id, 0, 0)[0], "ttl": r.ttl(container_id)}, 201

@app.route("/<username>/<training_name>", methods=["put"])
def update_training_info(username, training_name):
    #Author: LRL
    status = request.json["status"]
    username = unquote(username)
    training_name = unquote(training_name)
    if r.exists(username) == 0:
        return "", 404
    ok = 0
    for name in r.lrange(username, 0, -1):
        if name == training_name:
            ok = 1
            break
    if ok == 0:
        return "", 404
    # 根据<username>和<training_name>获取对应的main容器，main容器的id即为 training_id
    container = utils.get_container(username + "_" + training_name + "_main_1")
    training_id = container.id
    # 通过 docker-compose -f trainings/<training_name>/docker-compose.yml -p <username>_<training_name> COMMAND，启动或停止对应的training
    r = redis.Redis(db.redis_conn_pool)

    if status == 0:
        # 修改其在redis中对应的status，key：<training_id>，value为对应的状态码，1表示正在运行，0表示已停止
        r.rpop(training_id)
        r.rpush(training_id, 0)
        cmd = "docker-compose -f ./trainings/" + training_name + "/docker-compose.yml -p " + username + "_" + training_name + " down"
        os.system(cmd)
        # 返回
        return {"training_id": training_id, "status": 0, "ttl": r.ttl(training_id)}, 201
    else:
        r.rpop(training_id)
        r.rpush(training_id, 1)
        cmd = "docker-compose -f ./trainings/" + training_name + "/docker-compose.yml -p " + username + "_" + training_name + " up -d"
        os.system(cmd)
        return {"training_id": training_id, "status": 1, "ttl": r.ttl(training_id)}, 201

@app.route("/<username>/<training_name>", methods=["delete"])
def remove_training(username, training_name):
    main_container = utils.get_container(username + "_" + training_name + "_main_1")
    container_id = main_container.id
    if main_container is not None:
        os.system("docker-compose -f trainings/" + training_name + "/docker-compose.yml -p" + username + "_" + training_name + "down")
        r = redis.Redis(db.redis_conn_pool)
        pipe = r.pipeline()
        pipe.multi()
        pipe.lrem(username, 0,  training_name)
        pipe.delete(container_id)
        # pipe.hdel('trainging_id', container_id)
        pipe.execute()
        pipe.close()
        r.close()
        return "", 204
    else:
        return "", 404


@app.route("/trainings/<training_name>", methods=["get"])
def get_training_config(training_name):
    # 读取对应training的config.json文件
    # 返回
    ...

@app.route("/flags/<training_name>/<flag>", methods=["get"])
def verify_flag(training_name, flag):
    # 读取对应training的config.json文件中的flag，并返回
    # url中的某些特殊符号需要解码，所以调用unquote方法进行解码
    # 由于未明确返回数据格式，所以暂时返回true和false
    de_flag=unquote(flag)
    de_training_name=unquote(training_name)
    # 如果目录不存在就返回false
    if not os.path.exists("../trainings/" + de_training_name):
        return "" , 404

    with open("../trainings/" + de_training_name + "/config.json", "r") as f:
        std_read = json.load(f)
    # flag不正确就返回false
    if (de_flag != std_read["training"]["flag"]):
        return {"result":0} , 200
    # flag正确就返回true
    return {"result":1} , 200




@app.route("/entrances/<training_id>")
def entrance(training_id):
    """将请求转发至对应的容器"""
    ...