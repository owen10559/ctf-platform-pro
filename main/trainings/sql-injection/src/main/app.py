import flask
import urllib.parse
import pymysql

from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def index():
    cursor = pymysql.connect(host="mysql", user = "root", passwd = "", db = "db").cursor()
    password = request.args.get("password")
    if password:
        sql = "select password from fl4g where username = 'root' and password = '%s';" % password
        try:
            if cursor.execute(sql):
                return str(cursor.fetchall()[0][0])
            else:
                return "Password incorrect!"
        except Exception as e:
            return str(e)
    else:
        return "Do you know the password of user root?\nPlease GET me the password.\n"

if __name__ == "__main__":
    with open("/root/status", "w") as f:
        f.write("1")
    app.run(host="0.0.0.0")