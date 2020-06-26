from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from flask_cors import CORS
import base64
import json
import os
import sys


def get_frames(img_dir):
    print('get it !!!')

    img_streams, times = return_img_stream(img_dir)
    dic = {'imgs': img_streams, 'times': times}
    return dic  # json.dumps(dic,ensure_ascii=False)


def getTime(a):
    key = int(a.split('_')[1].split('.')[0])
    return key


def return_img_stream(img_local_paths='frames/'):
    img_streams = []
    times = []
    paths = os.listdir(img_local_paths)
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
