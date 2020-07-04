# Mulan_Server

## 环境
python 3.6

requirements.txt may be used to create an environment using(里面的依赖可能有不需要的):

`$ conda create --name <env> --file <this file>`
 
schema.sql是数据库初始化，在命令行运行：

`$ flask init-db`

使用pycharm的话数据源选择SQLite

## 运行程序：
`python manager.py`

## video.py中的路径是video存储路径
def generate_path(url):
    # 这个路径需要更换
    video_path = "/Users/guruoying/video"