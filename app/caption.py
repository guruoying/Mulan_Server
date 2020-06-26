from flask_cors import CORS

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)

server = Blueprint('caption', __name__, url_prefix='/caption')

CORS(server)


@server.route('/get_caption', methods=('GET', 'POST'))
def get_caption():
    if request.method == 'GET':
        return jsonify(video_id="123",
                       start_time="666", end_time="777", context="hello world!", count="0", emphasis="false")
