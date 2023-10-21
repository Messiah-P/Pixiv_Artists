import requests

import get_following
import traversal
from get_single_pic import SinglePic
from search import Artist
from multi_thread_download import multi_download

from config import ARTISTS_DIR, LOGO_PIXIV, HEAD_BARK
from log import log_output

def get_illust(artists_list, existed_pids):
     # 通过输入构造目录
     bark_new = '--更新画作--'
     bark_null = '--未更新--'
     for i in range(len(artists_list)): #遍历行
         artist_name = artists_list[i][0]
         uid = artists_list[i][1]
         log_output(f"画师:{artist_name} - {uid}")
         pic = SinglePic()
         pic.mkdir()
         # 创建对象获取该画师插画列表
         log_output(f"正在获取{artist_name}的插画...")
         artist = Artist(uid)
         pids_list = list(artist.get_pids(existed_pids))
         if len(pids_list) != 0:
             log_output(f"{artist_name}共有{str(len(pids_list))}件作品未下载, 开始下载{artist_name}的作品...")
             bark_info = ('画师: ' + artist_name + '\n' +'更新数: ' + str(len(pids_list)))
             bark_new = bark_new + '\n' + bark_info
             #创建多线程下载
             log_output(f"创建多线程下载...")
             multi_download(pids_list, 0)
         else:
             log_output(f"{artist_name}没有作品更新。")
             bark_null = bark_null + '\n' + artist_name
     bark = bark_new + '\n' + bark_null
     with requests.Session() as ret:
        bark = ret.get('%s/Pixiv画师更新/%s?icon=%s&group=画师' % (HEAD_BARK, bark, LOGO_PIXIV))
     print('\n下载结束啦')

if __name__ == '__main__':
    f = get_following.GetFollowing()
    #获取关注列表
    artists_list = f.update_userlist()
    print(artists_list)
    existed_pids = traversal.all_pids(ARTISTS_DIR)
    get_illust(artists_list, existed_pids)
