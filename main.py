import os
from flask import Flask, render_template, request


app = Flask(__name__)
@app.route('/')
def start():
    return render_template("start.html")


@app.route('/ques', methods=["POST", "GET"])
def base():
    return render_template("base.html")


if __name__ == "__main__":
    app.run(port=8033, host="127.0.0.1")

'''if __name__ == "__main__":
    db_session.global_init("db/service.db")
    db_sess = db_session.create_session()
    db_sess.commit()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)'''