import json
import config
import os
import redis
import containers
import flask
import db

app = flask.Flask("__main__")
client = containers.client

@app.route("/test")
def test():
    return "ok"

@app.route("/<username>/<training_name>", methods=["get"])
def get_training_info(username, training_name):
    # Author: LRL
    try:
        if username == "" or training_name == "":
            return "", 400

        # 根据<username>和<training_name>获取对应的main容器
        r = db.get_redis_conn()
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
        ret = ""
        if r.exists(training_id):
            ret = {"training_id": training_id, "status": eval(r.get(training_id)), "ttl": r.ttl(training_id)}
        r.close()
        if ret == "":
            return "", 404
        return ret, 200
    except Exception as e:
        app.log_exception(e)
        return "", 500

@app.route("/<username>/<training_name>", methods=["post"])
def create_training(username, training_name):
    # Author: LRL
    try:
        if username == "" or training_name == "":
            return "", 400
        if not os.path.exists("./trainings/" + training_name):
            return "", 404

        # 通过 docker-compose -f trainings/<training_name>/docker-compose.yml -p <username>_<training_name> up -d 启动对应的training
        cmd = "docker-compose -f ./trainings/" + training_name + "/docker-compose.yml -p " + username + "_" + training_name + " up -d"
        os.system(cmd)

        # 根据<username>和<training_name>获取对应的main容器
        container = containers.get_container(username + "_" + training_name + "_main_1")
        # main容器的id即为 training_id
        container_id = container.id

        # 将以下数据存入redis：
        # 用户拥有的training：key：<username>:trainings，value：[]，此处的value是一个列表，因此需要以类似于append的方式存入
        ttl = config.config["trainings"]["ttl"]
        r = db.get_redis_conn()
        pipe = r.pipeline()
        pipe.multi()
        pipe.rpush(username, training_name)

        # training_id的status及其ttl：key：<training_id>，value：1，ttl：***，ttl具体数值从config["trainings"]["ttl"]中读取
        if not r.exists(container_id):
            pipe.set(container_id, 1)
            pipe.expire(container_id, ttl)
        pipe.execute()
        ret = {"training_id": container_id, "status": eval(r.get(container_id)), "ttl": r.ttl(container_id)}
        r.close()

        # 返回
        return ret, 201
    except Exception as e:
        app.log_exception(e)
        return "", 500

@app.route("/<username>/<training_name>", methods=["put"])
def update_training_info(username, training_name):
    #Author: LRL
    try:
        if flask.request.form.get("status") == "":
            return "", 400
        status = int(flask.request.form.get("status"))

        if username == "" or training_name == "" or (status != 0 and status != 1):
            return "", 400

        r = db.get_redis_conn()
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
        training_id = 0
        for container in client.containers.list(all=True):
            if container.name == username + "_" + training_name + "_main_1":
                training_id = container.id
                break

        if training_id == 0:
            return "", 404
        # 通过 docker-compose -f trainings/<training_name>/docker-compose.yml -p <username>_<training_name> COMMAND，启动或停止对应的training
        # assert (status == 0 or status == 1)
        # 修改其在redis中对应的status，key：<training_id>，value为对应的状态码，1表示正在运行，0表示已停止
        ttl = config.config["trainings"]["ttl"]
        pipe = r.pipeline()
        if r.exists(training_id):
            ttl = r.ttl(training_id)
        pipe.set(training_id, status)
        pipe.expire(training_id, ttl)
        cmd = ""
        if status == 0:
            cmd = "docker-compose -f ./trainings/" + training_name + "/docker-compose.yml -p " + username + "_" + training_name + " stop"
        else:
            cmd = "docker-compose -f ./trainings/" + training_name + "/docker-compose.yml -p " + username + "_" + training_name + " start"
        os.system(cmd)
        pipe.execute()
        ret = {"training_id": training_id, "status": status, "ttl": r.ttl(training_id)}
        r.close()
        # 返回
        return ret, 201
    except Exception as e:
        app.log_exception(e)
        return "", 500

@app.route("/<username>/<training_name>", methods=["delete"])
def remove_training(username, training_name):
    # Author: dxw
    try:
        if username == "" or training_name == "":
            print("名称不得为空！")
            return "", 400

        main_container = containers.get_container(username + "_" + training_name + "_main_1")
        if main_container is not None:
            container_id = main_container.id
            os.system("docker-compose -f trainings/" + training_name + "/docker-compose.yml -p" + username + "_" + training_name + "down")
            r = db.get_redis_conn()
            pipe = r.pipeline()
            pipe.multi()
            pipe.lrem(username, 0,  training_name)
            # pipe.hdel('trainging_id', container_id)
            pipe.delete(container_id)
            pipe.execute()
            pipe.close()
            r.close()
            return "", 204
        else:
            return "", 404
    except Exception as e:
        app.log_exception(e)
        return "error", 500

@app.route("/trainings/<training_name>", methods=["get"])
def get_training_config(training_name):
    # Author:@LSC
    # 读取对应training的config.json文件
    # 返回
    try:
        if not os.path.exists("./trainings/"+training_name):
            return "" , 404
        if not os.path.exists("./trainings/"+training_name+"/config.json"):
            return "" , 404
        with open("./trainings/"+training_name+"/config.json") as f:
            config = json.load(f)
        config["training"].pop("flag")
        return config["training"], 200
    except Exception as e:
        app.log_exception(e)
        return "" , 500

@app.route("/flags/<training_name>", methods=["get"])
def verify_flag(training_name):
    # LSC
    # 读取对应training的config.json文件中的flag，并返回
    # 由于未明确返回数据格式，所以暂时返回true和false
    # 如果目录不存在就返回false
    try:
        de_flag=flask.request.args["flag"]
        de_training_name=training_name
        if not os.path.exists("./trainings/" + de_training_name):
            return "" , 404
        with open("./trainings/" + de_training_name + "/config.json", "r") as f:
            std_read = json.load(f)
        # flag不正确就返回false
        if (de_flag != std_read["training"]["flag"]):
            return {"result":0} , 200
        # flag正确就返回true
        else:
            return {"result":1} , 200
    except Exception as e:
        app.log_exception(e)
        return  "" , 500

@app.route("/entrances/<training_id>")
def entrance(training_id):
    """将请求转发至对应的容器"""
    ...
