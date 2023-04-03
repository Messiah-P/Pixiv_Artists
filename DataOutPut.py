import os

import FormatName
from HTMLDownloader import HTMLDownloader
from HTMLParser import HTMLParser
import zipfile
import imageio
import ModifyTime

class DataOutPut(object):
    def __init__(self):
        self.count = 0

    def mkdir(self, file_path):
        # 创建文件夹
        folder = os.path.exists(file_path)
        if not folder:
            os.makedirs(file_path)

    def is_download(self, resource, min_count):
        # 如果收藏数大于min_count就下载
        if resource[2] >= int(min_count):
            return True
        else:
            return False

    def download_img(self, resource, min_count, file_path):
        # 判断是否要下载
        if self.is_download(resource, min_count):
            # 判断是动图还是静图
            if resource[1]:
                # 下载动图
                self.ugoira_download(resource, file_path)
            else:
                # 下载静图
                self.static_download(resource, file_path)

    def get_file_name(self, file_url):
        # 通过文件路径获取文件名
        x = file_url.split('/')
        return x[-1]

    def download_file(self, id, file_url, file_path, resource):
        # 从resource获取插画信息
        userName = resource[5]
        illustTitle = resource[6]
        createDate = resource[7]
        # 将文件二进制保存为本地文件
        # 获取插画二进制数据
        content = HTMLDownloader.get_content(id, file_url)
        # 截取文件名
        pid = file_url.split('/')[-1].split('_')[0]
        suff = file_url.split('/')[-1].split('_')[1]
        # 替换画名中的'/'防止影响路径识别
        userName = FormatName.fileName(userName)
        illustTitle = FormatName.fileName(illustTitle)
        file_name = '/%s - %s - [pid=%s]-%s' % (userName, illustTitle, pid, suff)
        #file_name = HTMLDownloader.getSinglePic(id, file_url)
        file_path = os.path.join(file_path, userName)
        os.makedirs(file_path, 0o777, exist_ok=True)
        # 将二进制数据写入文件
        with open(file_path + file_name, mode='wb') as fw:
            fw.write(content)
            file_path_full = file_path + file_name
            ModifyTime.Modify(file_path_full, createDate)
        return file_name

    def open_zip(self, file_path, file_name, resource):
        # 从resource获取插画信息
        userName = resource[5]
        # 解压压缩包
        temp_file_list = []
        file_path = os.path.join(file_path, userName)
        open_path = file_path+file_name
        zipo = zipfile.ZipFile(open_path, "r")
        for img in zipo.namelist():
            temp_file_list.append(os.path.join(file_path+file_name.split('.')[0], img))
            zipo.extract(img, file_path+file_name.split('.')[0])
        zipo.close()
        return temp_file_list

    def create_gif(self, file_list, delays, file_path, resource, file_name):
        # 从resource获取插画信息
        userName = resource[5]
        createDate = resource[7]
        # 传入文件列表与延迟时间列表，合成gif
        file_path = os.path.join(file_path, userName)
        file_name = str(file_name.split('.')[0]) +'.gif'
        gif_file = file_path + file_name
        imgs = []
        delay_list = []
        num = 0
        for img in file_list:
            # 获取图片延迟时间
            delay_list.append(int(delays[num]['delay'])/1000)
            t = imageio.imread(img)
            imgs.append(t)
            num += 1
        # 合成gif文件
        imageio.mimsave(gif_file, imgs, "GIF", duration=delay_list)
        ModifyTime.Modify(gif_file, createDate)

    def ugoira_download(self, resource, file_path):
        # 下载动图
        # 获取动图压缩包和延迟时间
        illust_id = resource[0]
        h = HTMLParser()
        t = h.get_ugoira_resource(illust_id)
        if t is None:
            self.static_download(resource, file_path)
            return
        zip_file = t[0]
        delays = t[1]
        # 将压缩包下载到本地，获取压缩包名称
        file_name = self.download_file(illust_id, zip_file, file_path, resource)
        # 解压压缩包，获取解压后的文件列表
        file_list = self.open_zip(file_path, file_name, resource)
        # 合成gif
        self.create_gif(file_list, delays, file_path, resource, file_name)
        # 删除中间文件和文件夹
        for img in file_list:
            os.remove(img)
        file_path = os.path.join(file_path, resource[5])
        os.remove(file_path+file_name)
        file_name = file_name.split('.')[0]
        os.removedirs(file_path+file_name)

    def get_original_list(self, resource):
        # 根据作品页数与原图链接构造原图列表
        original_p0 = resource[4]
        pages = resource[3]
        original_list = []
        if pages != 1:
            li = original_p0.split('0.')
            for i in range(pages):
                original = li[0]+str(i)+'.'+li[1]
                original_list.append(original)
        elif pages == 1:
            original_list.append(original_p0)
        return original_list

    def static_download(self, resource, file_path):
        # 下载静图
        # 获取静态图的原图列表
        original_list = self.get_original_list(resource)
        # 遍历列表，下载列表中每个链接
        for url in original_list:
            self.download_file(resource[0], url, file_path, resource)




