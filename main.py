import time
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/getTime')
def getTime():
    return str(int(time.time()))

if __name__ == '__main__':
    app.run()