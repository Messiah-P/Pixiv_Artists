# 用于获取页面的HTML
import socket
import time

from requests.adapters import HTTPAdapter
import requests
from fake_useragent import UserAgent
from config import cookie
from log import log_output

repeat = 1
user_agent = UserAgent(verify_ssl=False).random


class HTMLDownloader():

    def get_resource(url, headers):
        retry = 1
        if url == '' or url is None:
            return
        while True:
            log_output(f"正在获取html源码...")
            try:
                with requests.Session() as s:
                    s.keep_alive = False
                    s.mount('http://', HTTPAdapter(max_retries=5))
                    s.mount('https://', HTTPAdapter(max_retries=5))
                    resource = s.get(url=url, headers=headers)
                    log_output(f"获取html源码成功！")
                    return resource
                    break
            except (requests.exceptions.RequestException, socket.timeout):
                log_output(f"获取html源码失败，正在进行第{retry}次重试...")
                time.sleep(3)
                retry += 1
                if retry > 5:
                    log_output(f"获取html源码失败，重试次数过多，已跳过。")
                    return False

    def get_html(url):
        # 获取html源码
        headers = {
            'user-agent': user_agent,
            'cookie': cookie
        }

        resource = HTMLDownloader.get_resource(str(url), headers)
        return resource.text

    def get_content(id, url):
        # 获取二进制数据
        headers = {
            'referer': 'https://www.pixiv.net/artworks/'+id,
            'user-agent': user_agent,
            'cookie': cookie
        }
        resource = HTMLDownloader.get_resource(url, headers)

        # 验证图片完整性
        flag = False
        if 'Content-Length' in resource.headers:
            if int(resource.headers['Content-Length']) == len(resource.content):
                flag = True
            else:
                flag = False

        if 'Transfer-Encoding' in resource.headers or flag:
            return resource.content
        else:
            return HTMLDownloader.get_content(id, url)
