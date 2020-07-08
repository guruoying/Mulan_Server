import base64
import functools
import os
import sys
import asyncio

import pysrt
import you_get
from .images.get_frame import get_frames
from .images.extractor import extract_images
from flask_cors import CORS

from flask import (
    Blueprint, request
)
from flask import jsonify

from app.db import get_db

server = Blueprint('video', __name__, url_prefix='/video')


def is_video_exists(url):
    db = get_db()
    if db.execute(
            'SELECT video_id FROM video WHERE url = ?', (url,)
    ).fetchone() is not None:
        return True
    return False


# 生成视频存贮路径
def generate_path(url):
    # 这个路径需要更换
    video_path = "/Users/sxz/code/code-2020/software/google_girls_hackathon/video_subtitle"
    if not os.path.exists(video_path):
        os.makedirs(
            "/Users/sxz/code/code-2020/software/google_girls_hackathon/video_subtitle")
    return video_path


# 下载视频
def download_video(url):
    path = generate_path(url)
    command = "you-get --format=flv360 -o " + path + " " + url
    # sys.argv = ['you-get', '--format=flv360', '--debug', '-o', path, url]
    # you_get.main()
    print(command)
    r = os.popen(command)
    info = r.readlines()  # 读取命令行的输出到一个list
    for line in info:  # 按行遍历
        l = str(line)
        if l.startswith("Downloading"):
            end = l.find(".flv") + 4
            file_name = l[12: end]
            return path + "/" + file_name  # video_path contains filename


# 生成字幕
def generate_caption(video_path, chinese=True, output_path="/Users/sxz/code/code-2020/software/google_girls_hackathon/subtitle"):
    # 默认为中文, 仅支持中英文
    if chinese == True:
        language = "cmn_hans_cn"
    else:
        language = "en"
    command = "autosub -i " + "\"" + video_path + "\"" +\
        " -ap -k -S " + language + " -of src -F srt -o " + output_path
    r = os.popen(command)
    video_name = video_path.split("/")[-1]
    video_name = video_name.rstrip(".flv")

    return output_path + "/" + video_name + "." + language + ".srt"


# 生成视频截图
def generate_image(video_path):
    img_local_paths = extract_images(video_path)
    # img_dir = '/Users/zhangqi/Desktop/for_google/girl_hackthon_2020/video_frame/demo'
    return get_frames(img_local_paths), img_local_paths


def getKey(a):
    key = int(a.split('_')[1])
    return key


def get_image(img_local_paths):
    return get_frames(img_local_paths)


CORS(server)


@server.route('/download_video', methods=('GET', 'POST'))
def download():
    if request.method == 'POST':
        url = request.args['url']
        print(url)
        db = get_db()
        if not is_video_exists(url):  # 建议加一个并且在路径中存在的条件
            video_path = download_video(url)
            print(video_path, url)
            db.execute(
                'INSERT INTO video (url, file_path) VALUES (?, ?) ',
                (url, video_path)
            )
            db.commit()
            return "download successfully"
        else:
            return "video exists"


@server.route('/get_image', methods=('GET', 'POST'))
def get_images():
    if request.method == 'POST':
        url = request.args['url']
        db = get_db()
        image_path = db.execute(
            'SELECT imagepath FROM video WHERE url = ?', (url,)
        ).fetchone()[0]
        if image_path is not None:
            image = get_image(image_path)
            return jsonify(image=image)
        else:
            video_path = db.execute(
                'SELECT file_path FROM video WHERE url = ?', (url,)
            ).fetchone()[0]
            # 这里有bug
            image, img_local_paths = generate_image(video_path)
            db.execute(
                'UPDATE video set imagepath = ? WHERE url = ?',
                (img_local_paths, url)
            )
            db.commit()
            return jsonify(image=image)


@server.route('/get_caption', methods=('GET', 'POST'))
def get_caption():
    if request.method == 'POST':
        url = request.args['url']
        db = get_db()
        video_id = db.execute(
            'SELECT video_id FROM video WHERE url = ?', (url,)
        ).fetchone()
        if video_id is not None:
            caption_rows = db.execute('SELECT start_time, end_time, content, count FROM caption WHERE video_id= ? ORDER BY start_time', (
                video_id[0],)
            )
            rows = caption_rows.fetchall()
            start = []
            end = []
            text = []
            count = []
            if rows != []:
                for caption_row in rows:
                    start.append(caption_row[0])
                    end.append(caption_row[1])
                    text.append(caption_row[2])
                    count.append(caption_row[3])
                return jsonify(video_id=video_id[0],
                               start_time=start, end_time=end, context=text, count=count)
            else:
                # 这里实现生成字幕
                # video_path = db.execute(
                #     'SELECT file_path FROM video WHERE url = ?', (url,)
                # ).fetchone()[0]
                video_path = "/Users/sxz/code/code-2020/software/google_girls_hackathon/video_subtitle/1.flv"
                caption_path = generate_caption(video_path)
                subs = pysrt.open(caption_path)
                for i in range(0, len(subs)):
                    start.append(subs[i].start.seconds +
                                 60 * subs[i].start.minutes)
                    end.append(subs[i].end.seconds + 60 * subs[i].end.minutes)
                    text.append(subs[i].text)

                    db.execute(
                        'INSERT INTO caption (video_id, start_time, end_time, content, count) VALUES (?, ?, ?, ?, 0)',
                        (video_id[0], start[i], end[i], text[i])
                    )
                return jsonify(video_id=video_id[0],
                               start_time=start, end_time=end, context=text, count="0")
        else:
            return "The video has not downloaded!"
