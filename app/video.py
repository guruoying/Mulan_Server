import base64
import functools
import os
import sys
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

def is_exists(url):
    db = get_db()
    if db.execute(
            'SELECT video_url FROM video_table WHERE video_url = ?', (url,)
    ).fetchone() is not None:
        return True
    return False

# 生成视频存贮路径
def generate_path(url):
    path = ""
    return path

# 下载视频
def download_video(url):
    path = generate_path(url)
    sys.argv = ['you-get', '--format=flv360', '-o', path, url]
    you_get.main()
    return path

# 生成字幕
def generate_caption(video_path):
    caption = ""
    return caption

#生成视频截图
def generate_image(viedo_path):
    img_dir = extract_images(viedo_path)
    #img_dir = '/Users/zhangqi/Desktop/for_google/girl_hackthon_2020/video_frame/demo'
    return get_frames(img_dir)


def getKey(a):
    key = int(a.split('_')[1])
    return key


def get_image(img_local_paths):
    img_streams = []
    paths = os.listdir(img_local_paths)
    paths.sort(key=getKey)
    for img_local_path in paths:
        if '.jpg' in img_local_path:
            path = img_local_paths + img_local_path
            with open(path, 'rb') as img_f:
                img_stream = img_f.read()
                img_stream = base64.b64encode(img_stream)
                img_stream = str(img_stream, "utf-8")
                img_streams.append(img_stream)
    return img_streams

CORS(server)
@server.route('/manager', methods=('GET', 'POST'))
def manager():
    if request.method == 'POST':
        url = request.args['url']
        print(url)
        db = get_db()
        if is_exists(url):
            print("enter")
            video_id = db.execute(
                'SELECT videoid FROM video_table WHERE video_url = ?', (url,)
            ).fetchone()[0]
            image_path = db.execute(
                'SELECT imagepath FROM image_table WHERE videoid = ?', (video_id,)
            ).fetchone()[0]
            image = get_image(image_path)
            subtitle = {}
            subtitle_rows = db.execute(
                'SELECT content,timestamp FROM caption_table WHERE videoid = ? ORDER BY timestamp', (video_id,)
            )
            for subtitle_row in subtitle_rows:
                content = subtitle_row[0]
                timestamp = subtitle_row[1]
                subtitle[timestamp] = content
            return jsonify(subtitle=subtitle,
                           image=image)
        else:
            video_path = download_video(url)
            caption = generate_caption(video_path)
            image = generate_image(video_path)
            #image = generate_image('/Users/zhangqi/Desktop/for_google/girl_hackthon_2020/video_frame/demo.mp4')
            db.execute(
                'INSERT INTO video (video_url, video_filepath, video_imagepath) VALUES (?, ?, ?)',
                (url, video_path, image)
            )
            db.commit()
            video_id = db.execute(
                'SELECT video_table FROM video_table WHERE video_url = ?', (url,)
            ).fetchone()[0]
            db.execute(
                'INSERT INTO video (imagepath, videoid) VALUES (?, ?)',
                (image, video_id)
            )
            # 此处字幕的数据库插入根据返回值修改
            # db.execute(
            #     'INSERT INTO caption_table (videoid, content, count, timestamp) VALUES (?, ?, ?, ?)',
            #     ()
            # )
            db.commit()
            return jsonify(caption=caption,
                           image=image)

#
# @server.route('/download', methods=('GET', 'POST'))
# def download():
#     if request.method == 'POST':
#         url = request.form['url']
#         if not is_exists(url):
#
#     return render_template('auth/register.html')
#
#
# @server.route('/subtitle', methods=('GET', 'POST'))
# def subtitle():
#     if request.method == 'POST':
#         url = request.form['url']
#         if not is_exists(url):
#     return 'Hello, download!!'
