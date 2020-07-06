import flask
from flask import request
from flask_cors import CORS
import base64
from flask import render_template
import json
import os
import sys

#server = flask.Flask(__name__)
# CORS(server)
# @server.route('/get_frames', methods=['get','post'])


def get_frames(img_dir):
    print('get it !!!')

    img_streams, times = return_img_stream(img_dir)
    dic = {'imgs': img_streams, 'times': times}
    return dic  # json.dumps(dic,ensure_ascii=False)


def getTime(a):
    key = int(a.split('_')[-1].split('.')[0])
    return key


def return_img_stream(img_local_paths):
    img_streams = []
    times = []
    paths = [img for img in os.listdir(img_local_paths) if '.jpg' in img]
    paths.sort(key=getTime)
    print(paths)
    for img_local_path in paths:
        if '.jpg' in img_local_path:
            path = os.path.join(img_local_paths, img_local_path)
            times.append(getTime(img_local_path))
            with open(path, 'rb') as img_f:
                img_stream = img_f.read()
                img_stream = base64.b64encode(img_stream)
                img_stream = str(img_stream, "utf-8")
                img_streams.append(img_stream)
    return img_streams, times


if __name__ == '__main__':
    server.run(port=2333, debug=True)
