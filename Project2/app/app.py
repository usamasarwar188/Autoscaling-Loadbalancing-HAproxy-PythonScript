from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "HostName <h1> Roll no: I16-0188 </h1>"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
