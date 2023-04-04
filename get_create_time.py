import os
import time

def ModifyFileTime(file_path, timestr):

    timestr = timestr.split('+')[0]
    strFormat = "%Y-%m-%dT%H:%M:%S"
    datetime_obj = time.mktime(time.strptime(timestr, strFormat))
    stinfo = os.stat(file_path)
    os.utime(file_path, (stinfo.st_mtime, datetime_obj))


def Modify(file_path, timestr):
    # 读配置，重新写配置
    # ReadXlsx(mConfigFile)
    # 读取新配置，修改文件的操作时间
    # SetFileOpTime(mPathFile)

    try:
        ModifyFileTime(file_path, timestr)
        #print(file_path)
        #print("修改时间成功", timestr)
    except:
        print(file_path)
        print("异常", timestr)
