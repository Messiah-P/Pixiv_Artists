# 用于获取页面的HTML
from requests.adapters import HTTPAdapter
import requests
from fake_useragent import UserAgent
from config import cookie

repeat = 1
user_agent = UserAgent(verify_ssl=False).random


class HTMLDownloader():

    def get_resource(url, headers):
        if url == '' or url is None:
            return
        s = requests.Session()
        s.keep_alive = False
        s.mount('http://', HTTPAdapter(max_retries=5))
        s.mount('https://', HTTPAdapter(max_retries=5))
        try:
            resource = s.get(url=url, headers=headers)
        except Exception:
            resource = HTMLDownloader.get_resource(url, headers)
        return resource

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
