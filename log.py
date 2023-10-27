import os
from conf.config import log_path, time_now

def log_output(msg):
    """
    将文本信息输出到控制台和日志文件中。
    """
    # 使用with open语句，避免忘记关闭文件流
    with open(log_path, 'a+') as l:
        log_msg = f"[{str(time_now).split('.')[0]}]{msg}"
        # 优化print的性能，减少I/O操作
        print(log_msg, file=l, flush=True)
        print(log_msg, flush=True)
        os.chmod(log_path, 0o777)
