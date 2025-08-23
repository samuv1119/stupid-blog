from flask import Flask, request, render_template, Blueprint
from dotenv import load_dotenv
import os
import model
import time

load_dotenv()
api_key = os.getenv("API_KEY")

status_data = model.StatusDataMgr()

interface = Blueprint("interface", __name__)

if len(status_data) < 1:
    status_data.append_status(status_data.create_status("初始记录", "这是第一条状态记录"))


@interface.route("/status_set", methods=['post'])
def api_status_set():
    provided_key = request.headers.get("X-API-KEY", "")
    if provided_key != api_key:
        return "fail 2 match key."
    status = request.args.get("status", "未获取")
    description = request.args.get("description", "思索中......")
    status = status_data.create_status(status, description)
    status_data.append_status(status)
    return f"success 2 set status 2 {status}"


@interface.route('/test')
def test():
    for i in range(50):
        item = status_data.create_status("test" + str(int(time.time() % 100)), "des" + str(int(i)))
        status_data.append_status(item)
    return f"item append success"

# @app.route("/cunter_set", methods=['post'])
# def api_test():
#     provided_key = request.headers.get("X-API-KEY", "")
#     if provided_key != api_key:
#         return "fail 2 match key."
#     global counter
#     counter += 1
#     return "success 2 increase counter."
