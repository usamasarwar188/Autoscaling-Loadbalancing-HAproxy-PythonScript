
from flask import Flask
import socket

app = Flask(__name__)


@app.route("/")
def home():
    return "<h2>Roll no: i160188</h2><h2>Hostname: {} </h2> ".format(socket.gethostname())


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
