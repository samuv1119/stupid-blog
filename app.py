from flask import Flask,request
from dotenv import load_dotenv 
import os

load_dotenv()

app = Flask(__name__)

api_key=os.getenv("API_KEY")

counter=0

@app.route('/')
def hello_world():
    return "Hello World! - by samuv."

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

if __name__ == "__main__":
    app.run()

