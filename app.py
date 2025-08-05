import sys
import time

from flask import Flask, request, render_template
from dotenv import load_dotenv
import os
import model


load_dotenv()

app = Flask(__name__)

api_key = os.getenv("API_KEY")

status_data=model.StatusDataMgr()

if len(status_data)<1:
    status_data.append_status(status_data.create_status("初始记录","这是第一条状态记录"))


# todo: 加入tinydb数据库来存储状态,历史状态,感想等信息

@app.route('/')
def hello_world():
    return f"Hello World! - by samuv."


@app.route('/test')
def test():
    item=status_data.create_status("test"+str(int(time.time()%100)),"des"+str(int(time.time()%1000)))
    status_data.append_status(item)
    return f"item append success"


@app.route("/cunter_set", methods=['post'])
def api_test():
    provided_key = request.headers.get("X-API-KEY", "")
    if provided_key != api_key:
        return "fail 2 match key."
    global counter
    counter += 1
    return "success 2 increase counter."


@app.route("/status_set", methods=['post'])
def api_status_set():
    provided_key = request.headers.get("X-API-KEY", "")
    if provided_key != api_key:
        return "fail 2 match key."
    present_status = request.args.get("status", "待设置")
    return f"success 2 set status 2 {present_status}"


@app.route("/test_index")
def test_index():
    present_status = status_data.get_present_status()
    history_status = status_data.get_history_status()
    return render_template("status-ds-4.html",present=present_status,history=history_status)


if __name__ == "__main__":
    app.run(debug=True)
