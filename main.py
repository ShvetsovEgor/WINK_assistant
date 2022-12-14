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
    import sqlite3
    con = sqlite3.connect("db_achievements.db")
    cur = con.cursor()
    user_id = 0
    ans = []
    f = []
    for i in range(8):
        prog = cur.execute(f"""SELECT prog{i} FROM users WHERE id = {user_id}""").fetchone()[0]
        max_value = cur.execute(f"""SELECT max_value FROM quests_params WHERE id = {i}""").fetchone()[0]
        ans.append([prog, max_value])
    for j in range(4):
        block_prog = cur.execute(f"""SELECT block_prog{j} FROM users WHERE id = {user_id}""").fetchone()[0]
        f.append(block_prog)

    return render_template("base.html", ans=ans, f=f)



if __name__ == "__main__":
    app.register_blueprint(apiserver.blueprint)
    app.run(port=8033, host="127.0.0.1")





