# coding=utf8
"""
封装的下载器,直接调用使用
time: 2020-05-11
author: coder_sakura
"""

import time
import requests

from conf.config import uid_cookie
from following.log_record import logger
from following.message import TEMP_MSG
# 强制取消警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# class Down(object):
class Downloader:
	def __init__(self):
		self.class_name = self.__class__.__name__
		self.se = requests.session()

		self.headers = {
			# "Connection": "keep-alive",
			"Host": "www.pixiv.net",
			"referer": "https://www.pixiv.net/",
			"origin": "https://accounts.pixiv.net",
			"accept-language": "zh-CN,zh;q=0.9",	# 返回translation,中文翻译的标签组
			"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
				'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
			"cookie": uid_cookie
		}
		# 作品链接
		self.artworks_url = "https://www.pixiv.net/artworks/{}"
		# 作品数据 8.16
		# self.ajax_illust = "https://www.pixiv.net/ajax/illust/{}"
		self.ajax_illust = "https://www.pixiv.net/touch/ajax/illust/details?illust_id={}"
		self.ajax_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "",
            "Connection": "keep-alive",

		}

		# print("user_id",self.client.user_id)

	def baseRequest(self, options, data=None, params=None, retry_num=5):
		'''
	    :params options: 请求参数,暂时只用到headers和url
	    :params data: Post
	    :params params: Get
	    :params retry_num: 重试次数
	    :return: response对象/False

	    列表推导式作用在于: 优先使用options中的headers,否则使用self.headers
	    比如:添加referer,referer需要是上一个页面的url,则可以自定义请求头
	    demo_headers = headers.copy()
	    demo_headers['referer']  = 'www.example.com'
	    options ={"url":"origin_url","headers":demo_headers}
	    baseRequest(options=options)
	    '''
		base_headers = [options["headers"] if "headers" in options.keys() else self.headers][0]

		try:
			# if options["method"].lower() == "get":
			# 网络请求函数get、post请求,暂时不判断method字段,待后续更新
			# logger.debug("cookie_list {}".format(len(self.cookie_list)))
			response = self.se.get(
	    			options["url"],
	    			data = data,
	    			params = params,
					headers = base_headers,
	    			verify = False,
	    			timeout = 10,
				)
			return response
		except  Exception as e:
			if retry_num > 0:
				logger.warning(TEMP_MSG["DM_RETRY_INFO"].format(options["url"]))
				time.sleep(1)
				return self.baseRequest(options,data,params,retry_num-1)
			else:
				logger.warning(TEMP_MSG["DM_NETWORK_ERROR_INFO"].format(self.class_name,options,e))
				return None


# Downloader = Down()