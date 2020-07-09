# Mulan_Server

## 环境

新建 conda 环境，建议 python 版本为 3.8：

`$ conda create -n <env_name> python=3.8`

然后切换到相应环境：

`$ conda activate <env_name>`

安装必须的依赖需要在该项目目录下运行以下指令:

`$ pip install -r requirements.txt`

schema.sql 是数据库初始化，如需初始化（非必要操作），可在命令行运行：

`$ flask init-db`

## 运行程序：

### 备注

app/video.py 中 21, 22 行的存储路径需更换，分别为`VIDEO_PATH` 和 `SUBTITLE_PATH`

### 运行指令

`python manager.py`
