import sys
import time
from pydoc import describe

import os
import model
import interface

from flask import Flask, Blueprint, render_template

app = Flask(__name__)

# 注册interface蓝图
app.register_blueprint(interface.interface, url_prefix='/api')

status_data = model.StatusDataMgr()


@app.route('/')
def hello_world():
    return index()

@app.route("/index")
def index():
    status_data.remove_old_status()
    present_status = status_data.get_present_status()
    history_status = status_data.get_history_status()
    return render_template("status-ds-4.html", present=present_status, history=history_status)

@app.route("/post")
def postpage():
    return render_template("post-ds-4.html")


if __name__ == "__main__":
    app.run(debug=True)

# todo:
#  1.加入时间段可视化
#  2.加入音乐分享页
#  3.加入关于信息页
