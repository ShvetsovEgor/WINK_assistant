import os
from flask import Flask, render_template, request
import eel
import apiserver

app = Flask(__name__)


@app.route('/')
def start():
    return render_template("start.html")


@app.route('/test')
def test():
    return render_template("another.html")


@app.route('/ques', methods=["POST", "GET"])
def base():
    return render_template("base.html")


if __name__ == "__main__":
    app.register_blueprint(apiserver.blueprint)
    app.run(port=8033, host="127.0.0.1")
