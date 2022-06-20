import pymysql
import os

from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def index():
    cursor = pymysql.connect(host="mysql", user = "root", passwd = "", db = "db").cursor()
    password = request.args.get("password")
    if password:
        sql = "select * from fl4g where username = 'root' and password = '%s';" % password
        try:
            if cursor.execute(sql):
                return "flag{login-bypass}"
            else:
                return "Password incorrect!"
        except Exception as e:
                return str(e)
    else:
        return "GET me the password of user root to login.\n"

if __name__ == "__main__":
    with open("/root/status", "w") as f:
        f.write("1")
    app.run(host="0.0.0.0")