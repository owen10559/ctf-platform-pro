FROM python:3.8

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --upgrade pip
RUN pip install flask
RUN pip install pymysql

EXPOSE 5000

CMD python /root/app.py