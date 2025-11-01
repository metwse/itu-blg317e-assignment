from flask import Flask
import time


def create_app():
    start = time.time()

    def status():
        return {
            "message": "OK",
            "uptime": int(time.time() - start)
        }

    app = Flask(__name__)

    app.add_url_rule("/", view_func=status)

    return app
