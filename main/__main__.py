import flask
import apis

app = flask.Flask(__name__)

@app.route("/test")
def test():
    return "ok"

@app.route("/<username>/<training_name>", methods=["get"])
def start(username, training_name):
    return apis.start(username, training_name)

@app.route("/<username>/<training_name>", methods=["delete"])
def stop(username, training_name):
    return apis.stop(username, training_name)

@app.route("/flag/<training_name>/<flag>", methods=["get"])
def verify(training_name, flag):
    apis.verify(training_name, flag)

def training_monitor():
    """
    通过多线程循环执行，循环周期由配置文件决定
    1.遍历所有的容器（包括已经停止的），根据容器名（以<username>_<training>的格式作为开头）查询其对应的training在redis中的记录。
    若redis中不存在该training对应的记录，则将该容器移除
    2.遍历所有正在运行的training，若其对应的某个容器已经停止，则重启（先remove再start）该training
    """

if __name__ == "__main__":
    ... # 通过多线程执行函数
    app.run("0.0.0.0")