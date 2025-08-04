from flask import Flask,request
from dotenv import load_dotenv 
import os

load_dotenv()

app = Flask(__name__)

api_key=os.getenv("API_KEY")

counter=0
status="待设置"

@app.route('/')
def hello_world():
    return f"Hello World! - by samuv.\n\r\n\rsamuv 现在的状态是:{status}"

@app.route('/test')
def show_counter():
    return f"the counter has touched {counter} times."

@app.route("/cunter_set",methods=['post'])
def api_test():
    provided_key=request.headers.get("X-API-KEY","")
    if provided_key != api_key:
        return "fail 2 match key."
    global counter
    counter+=1
    return "success 2 increase counter."

@app.route("/status_set",methods=['post'])
def api_status_set():
    provided_key=request.headers.get("X-API-KEY","")
    if provided_key != api_key:
        return "fail 2 match key."
    global status
    status=request.args.get("status","待设置")
    return f"success 2 set status 2 {status}"


if __name__ == "__main__":
    app.run(debug=True)

