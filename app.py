from flask import Flask
import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
    return 'Flask Apache server is UP!!! <br><br>Web App is running! <br><br>Current date-time: ' + str(datetime.datetime.now())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
