#!/usr/bin/env python3

from flask import Flask, request, abort, jsonify, render_template, make_response

import json
import http
import smtplib
import subprocess
from email.message import EmailMessage
from email.parser import HeaderParser
from email.policy import default
import logging
import socket

# Override server header
http.server.BaseHTTPRequestHandler.version_string = lambda x: "fnord"

# Configure Logging
logger = logging.getLogger(__name__)
fileLog = logging.FileHandler(filename="webhook.log", encoding='utf-8')
fileLog.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fileLog.setFormatter(formatter)
logger.addHandler(fileLog)
logger.setLevel(logging.DEBUG)

# Flask: Go
app = Flask(__name__)


@app.route('/hook/<path:subpath>', methods=['POST'])
def get_webhook(subpath):
    try:
        logger.debug('received data:' + repr(request.json))
        sendMail(subpath, request.json)
        return 'success', 200
    except Exception as e:
        print("Exception occured:", repr(e))
        print(request.is_json, request.get_data())
    abort(400)


@app.route('/<path:subpath>', methods=["GET"])
def get(subpath):
    return "You monster", 400


@app.route("/ping")
def ping():
    return jsonify({"status": 200, "msg": "Pong"})


def sendMail(template, data):
    msg = EmailMessage()
    email = render_template('webhook.'+template, **data)
    p = HeaderParser(policy=default).parsestr(email)

    # Copy headers
    for h, v in p.items():
        msg[h] = v

    # Copy body
    msg.set_content(p.get_content())

    sendmail_location = "/usr/sbin/sendmail"
    subprocess.run([sendmail_location, "-t", "-oi"], input=msg.as_bytes())


if __name__ == '__main__':
    app.run(debug=False, use_debugger=False, use_reloader=False, port=3000, host='0.0.0.0')

