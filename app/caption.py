from flask_cors import CORS
import srt
import pysrt

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)

server = Blueprint('caption', __name__, url_prefix='/caption')

CORS(server)
srt_dir = "demo.cmn_hans_cn.srt"


@server.route('/get_caption', methods=('GET', 'POST'))
def get_caption():
    subs = pysrt.open(srt_dir)
    start = []
    end = []
    text = []
    for i in range(0, len(subs)):
        start.append(subs[i].start.seconds + 60 * subs[i].start.minutes)
        end.append(subs[i].end.seconds + 60 * subs[i].end.minutes)
        text.append(subs[i].text)

    if request.method == 'GET':
        return jsonify(video_id="1",
                       start_time=start, end_time=end, context=text, count="0")


if __name__ == "__main__":
    get_caption()
