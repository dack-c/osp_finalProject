from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')  # Initial 웹사이트


if __name__=='__main__':
    ipAddress="127.0.0.1"
    print("Starting the service with ipAddress = " + ipAddress)
    listen_port = 5555

    app.run(debug=False, host = ipAddress, port=int(listen_port))


    