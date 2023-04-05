# 多线程下载图片
import threading
from threading import Thread

from html_parser import HTMLParser
from get_single_pic import SinglePic
import math
from retrying import retry

count = 0
glob_lock = threading.Lock()

#@retry(stop_max_attempt_number=3)
def download(illust_ids, min_count, id_count):
    global count
    # 下载id列表中的所有图片
    h = HTMLParser()
    d = SinglePic()
    for illust in illust_ids:
        resource = h.get_resource(illust)
        d.download_img(resource, min_count)
        glob_lock.acquire()
        count += 1
        num = round(count/id_count*100, 2)
        print('\r下载进度:'+str(num)+'/100', end="")
        glob_lock.release()



def multi_download(pids_list, min_count):
    # 多线程下载图片
    # 默认线程总数
    thread_count = 48
    # id总数
    id_count = len(pids_list)
    # 设置线程数
    if id_count < thread_count:
        thread_count = id_count
    else:
        thread_count = thread_count

    # 每个线程要分配的id数量
    d = math.ceil(id_count/thread_count)
    # 声明线程列表
    threads = []
    for i in range(thread_count - 1):
        t = Thread(target=download, args=(pids_list[i * d:(i + 1) * d], min_count, id_count))
        threads.append(t)
        t.start()
    t = Thread(target=download, args=(pids_list[(thread_count - 1) * d:id_count], min_count, id_count))
    threads.append(t)
    t.start()
    for t in threads:
        t.join()
