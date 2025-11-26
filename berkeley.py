################################################################################

import datetime as dt
import threading, random

from Master import Master
from Client import Client

from flask import Flask, jsonify, render_template

################################################################################

app = Flask(__name__)

################################################################################

port = 8888
clients:list[Client] = []

master = Master(port, clients)
for idx in range(8): clients.append(Client(idx, port))

################################################################################

@app.route("/")
def home():
    return render_template("berkeley.html")

@app.route("/state")
def state():
    time = dt.datetime.now();
    date = dt.datetime(time.year, time.month, time.day)

    return jsonify([{
        'idx': client.idx,
        'time': (client.current_time - date).total_seconds(),
        'diffs': client.diffs,
        'speed': client.speed,
    } for client in master.clients])

@app.route("/skew/<int:idx>")
def clock_skew(idx:int):
    master.clients[idx].clockSkew()
    return ''

@app.route("/drift/<int:idx>")
def drift_rate(idx:int):
    master.clients[idx].driftRate()
    return ''

################################################################################

if __name__ == '__main__':
    app.run(debug=False, port=5000)

################################################################################
