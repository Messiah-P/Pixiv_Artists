# 说明
pixiv爬虫，爬取pixiv画师的插画作品

## 文件结构
```
.                       # 插画存放根目录
|-- Folder1             # 画师名
    |-- xxx.jpg         # 插画名
|-- Folder2             # 画师名
    |-- 1480420.txt     # 插画名
|-- Folder3             # 画师名
    |-- 28440744.txt    # 插画名
.                       # 脚本根目录
|-- SpiderMain.py       # Python 爬虫脚本
```

# 运行环境
已测试:  
macOS Ventura 13.2, python3.9  
Debian, python2.7.18


# 使用方法
1. 安装python
2. 安装python库
3. 下载本项目代码
4. 浏览器登录pixiv后复制cookie粘贴到HTMLDownloader.py中
5. 在SpiderMain.py中修改图片的保存路径
6. 在Pixiv.xls中增加画师名和uid
7. python SpiderMain.py 运行程序
8. 若遇到下载问题，请尝试将pixiv账号的r18与r18g开关打开

# 更新
## 23.01.26
1. 格式化图名：作者名 - 图名 - [pid=104012083]-p0.jpg
2. 通过pid增加去重功能，只检测插画更新，防止重复下载
3. 使用fake_useragent反爬
4. 读取Pixiv.xls文件中作者信息，方便批量更新

# 声明

代码基于plasma的[Pixivspider](https://github.com/plasmacookie/pixivSpider)项目
