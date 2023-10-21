# coding=utf8
"""
关注画师爬虫
time: 2020-05-11
author: coder_sakura
"""
import json
import re

from following.downer import Downloader
from following.log_record import logger
from following.message import TEMP_MSG
from config import uid


class Crawler(object):
    def __init__(self):
        self.u_list = []
        self.Downloader = Downloader()
        self.user_id = uid
        self.base_request = self.Downloader.baseRequest

        # 公开/非公开 见get_page_users
        self.rest_list = ["show", "hide"]
        # 画师列表
        self.follw_url = "https://www.pixiv.net/ajax/user/{}/following".format(self.user_id)
        #self.follw_url = "https://www.pixiv.net/users/17254955/following"
        # 作品链接,存数据库
        self.artworks_url = "https://www.pixiv.net/artworks/{}"
        # 画师作品列表
        self.all_illust_url = "https://www.pixiv.net/ajax/user/{}/profile/all"
        self.class_name = self.__class__.__name__

    def get_page_users(self, offset, rest="show"):
        """
        :params offset 偏移量,按照偏移量获得limit范围内的画师
        :return 接口数据中的画师数组
        """
        params = {
            "offset": offset,
            "limit": 100,
            "rest": rest,
        }
        try:
            r = json.loads(self.base_request({"url": self.follw_url}, params=params).text)
            #print(r)
        except Exception as e:
            # 网络请求出错
            logger.warning(TEMP_MSG["FOLLOW_PAGE_ERROR_INFO"].format(self.class_name, offset, offset + 100))
            logger.warning(f"<Exception> - {e}")
            return None
        else:
            # 未登录
            if r["message"] == TEMP_MSG["UNLOGIN_TEXT"]:
                logger.warning(TEMP_MSG["UNLOGIN_INFO"].format(self.class_name))
                return TEMP_MSG["UL_TEXT"]

            res = r['body']['users']
            return res

    def get_users(self):
        """
        :return: 所有关注画师的uid,userName,latest_id(最新的pid)
        :[{"uid":uid,"userName":userName,"latest_id":latest_id},...]
        """
        offset = 0
        users_info_list = []
        err_count = 0
        err_limit = 10

        for rest in self.rest_list:
            while True:
                u_list = self.get_page_users(offset, rest=rest)

                # 网络请求出错
                if u_list == None:
                    # 累计10次网络错误
                    if err_count < err_limit:
                        offset += 100
                        err_count += 1
                        continue
                    else:
                        break

                # 未登录
                if u_list == TEMP_MSG["UL_TEXT"]:
                    users_info_list = TEMP_MSG["UL_TEXT"]
                    break

                # 获取所有关注完毕
                if u_list == []:
                    break

                for u in u_list:
                    user_info = {}
                    user_info["uid"] = int(u["userId"])
                    # userName = re.sub('[\\\/:*?"<>|]','_',u["userName"])
                    userName = re.sub(r'[\s\/:*?"<>|\\]', '_', u["userName"])
                    user_info["userName"] = userName

                    # 画师/用户无作品
                    if u["illusts"] == []:
                        user_info["latest_id"] = -1
                        logger.warning(
                            TEMP_MSG["FOLLOW_NO_ILLUSTS_INFO"].format(self.class_name, u["userName"], u["userId"]))
                    # 无作品不做动作
                    # continue
                    else:
                        user_info["latest_id"] = int(u["illusts"][0]["id"])

                    users_info_list.append(user_info)
                offset += 100

        return users_info_list

    def get_user_illust(self, u):
        """
        :params u: 画师信息--字典
        :return user_illust_list: 画师信息包括:uid,userName,latest_id,path
        """
        u["path"] = self.file_manager.mkdir_painter(u)
        illust_url = self.all_illust_url.format(u["uid"])
        try:
            u_json = json.loads(self.base_request({"url": illust_url}).text)["body"]
            i = u_json.get("illusts", [])
            m = u_json.get("manga", [])
            # 列表推导式合并取keys,转为list
            user_illust_list = list([dict(i) if len(m) == 0 else dict(i, **m)][0].keys())
        except Exception as e:
            logger.warning(TEMP_MSG["FOLLOW_DATA_ERROR_INFO"].format(self.class_name, e))
            return []
        else:
            return user_illust_list

    @logger.catch
    def run(self):
        # 开始工作
        TAG_FLAG_USER = False
        logger.info(TEMP_MSG["BEGIN_INFO"].format(self.class_name))
        try:
            u_list = self.get_users()
            print(u_list)
        except Exception as e:
            logger.warning(TEMP_MSG["FOLLOW_ERROR_INFO"].format(self.class_name))
            logger.warning(f"<Exception> - {e}")
            logger.warning(TEMP_MSG["SLEEP_INFO"].format(self.class_name))
            return
        else:
            if u_list != []:
                logger.success(TEMP_MSG["FOLLOW_SUCCESS_INFO"].format(self.class_name, len(u_list)))
            # 关注列表为空
            elif u_list == []:
                logger.warning(TEMP_MSG["NO_FOLLOW_USERS"].format(self.class_name))
                return
            # 未登录
            elif u_list == TEMP_MSG["UL_TEXT"]:
                logger.warning(TEMP_MSG["UNLOGIN_INFO"].format(self.class_name))
                exit()

            TAG_FLAG_USER = True

        # ======================================
        return u_list
        logger.info("=" * 48)
        logger.info(TEMP_MSG["SLEEP_INFO"].format(self.class_name))
"""
if __name__ == '__main__':
  c = Crawler()
  while True:
    c.run()
"""

