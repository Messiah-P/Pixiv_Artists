import datetime
import yaml

# 读取YAML文件
with open("/mnt/python/Pixiv_Artists/config.yml", "r") as f:
    config = yaml.safe_load(f)

# 获取Headers配置
headers = config["headers"]
cookie = headers["cookie"]
referer = headers["referer"]

# 获取Paths配置
paths = config["paths"]
ARTISTS_DIR = paths["artists_dir"] #插画的保存路径
artists_info = paths["artists_info"]
LOG_PATH = paths["log_path"]

# 链接配置
links = config["links"]
LOGO_PIXIV = links["logo_pixiv"]
HEAD_BARK = links["head_bark"]

#其他信息
time_now = datetime.datetime.now()
time_yesterday = time_now + datetime.timedelta(days=-1)
log_path = f"{LOG_PATH}/{datetime.datetime.now():%Y-%m-%d}.log"


