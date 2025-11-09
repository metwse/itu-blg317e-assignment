from flask import jsonify
import time


class StatusHandler:
    def __init__(self, start_time):
        self.start_time = start_time

    def get_status(self):
        return jsonify({"message": "OK", "uptime": int(time.time() - self.start_time)})
