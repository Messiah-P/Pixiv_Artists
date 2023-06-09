# 通过输入的信息来获取作品id
from html_downloader import HTMLDownloader
import json
import math
import re
from retrying import retry
from threading import Thread
from queue import Queue


class Artist(object):
    def __init__(self, userid):
        # 初始化对象时传入画师id
        # 将其自动转换成获取作品id的url
        self.search_url = "https://www.pixiv.net/ajax/user/" + userid + "/profile/all?lang=zh"

    @retry(stop_max_attempt_number=3)
    def get_illust_ids(self, deduplicate_list):
        # 返回有作品id的集合
        # 获取json格式的字符串
        h = HTMLDownloader.get_html(self.search_url)
        # 将json格式的字符串转换成字典格式
        j = json.loads(h)
        # 获取包含插画id的字典
        illusts = j["body"]['illusts']
        illust_ids = set()
        # 如果illusts不为空
        if illusts:
            # 循环illusts，并将作品id放入集合中,去重
            for illust in illusts:
                if illust not in deduplicate_list:
                    illust_ids.add(illust)
        return illust_ids


class Tags(object):
    def __init__(self, tag, mode):
        # 初始化时传入要搜索的内容与限制级
        self.tag = tag
        self.mode = mode
        self.count = 0

    def get_illust_count(self):
        # 使用tag和mode构造出能够获取总作品数的链接
        url = 'https://www.pixiv.net/tags/' + self.tag + '/illustrations?mode=' + self.mode+'&s_mode=s_tag'
        # 获取搜索的作品总数
        h = HTMLDownloader.get_html(url)
        p1 = re.compile('\\d*件投稿されています')
        p2 = re.compile('\\d*')
        # 获取xx件投稿されています这句话
        s = p1.search(h).group()
        # 从句子中获取数字
        illust_count = int(p2.search(s).group())
        return illust_count

    def get_total_page(self):
        # 获取搜索内容的总页数

        # 获取作品总数
        illust_count = self.get_illust_count()
        # 获得总页数
        if illust_count/60 > 1000:
            total_page = 1000
        else:
            total_page = int(math.ceil(illust_count/60))
        return total_page

    def get_one_illust_ids(self, p, total_page):
        # 获取某一页作品的id集合

        self.count += 1
        num = round(self.count/total_page*100, 2)
        if num > 100:
            print('\r搜索进度:100.0/100', end="")
        else:
            print('\r搜索进度:'+str(num)+'/100', end="")

        url = 'https://www.pixiv.net/ajax/search/illustrations/' + self.tag + '?mode=' + self.mode + '&p=' + str(p)
        h = HTMLDownloader.get_html(url)
        j = json.loads(h)
        datas = j['body']['illust']['data']
        illust_ids = set()
        if datas:
            for data in datas:
                illust_id = data['id']
                illust_ids.add(illust_id)
        return illust_ids

    def add_ids(self, start, end, q, total_page):
        # 将从start页到end页的数据存入队列q中
        illust_ids = set()
        for i in range(start, end):
            ids = self.get_one_illust_ids(i+1, total_page)
            illust_ids = illust_ids.union(ids)
        q.put(illust_ids)

    def get_illust_ids(self):
        # 默认线程总数
        t_count = 128
        # 总页数
        total_page = self.get_total_page()
        # 设置线程数
        if total_page < t_count:
            thread_count = total_page
        else:
            thread_count = t_count

        # 每个线程要爬取的页数
        d = math.ceil(total_page/thread_count)
        # 声明队列
        q = Queue()
        # 声明线程列表
        threads = []
        # 执行前127个线程
        for i in range(thread_count-1):
            t = Thread(target=self.add_ids, args=(i*d, (i+1)*d, q, total_page))
            threads.append(t)
            t.start()
        # 执行最后一个线程
        t = Thread(target=self.add_ids, args=((thread_count-1)*d, total_page, q, total_page))
        threads.append(t)
        t.start()
        for t in threads:
            t.join()
        # 声明集合
        illust_ids = set()
        # 将队列中的多个集合合并为一个集合
        for _ in range(thread_count):
            illust_ids = illust_ids.union(q.get())
        return illust_ids
