# 用于获取页面的HTML
from requests.adapters import HTTPAdapter
import requests
from fake_useragent import UserAgent

repeat = 1
cookie = '__utma=235335808.1116251316.1674396762.1674619254.1674633889.5; __utmb=235335808.5.9.1674633905244; __utmc=235335808; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=90529190=1^9=p_ab_id=1=1^10=p_ab_id_2=4=1^11=lang=zh=1; __utmz=235335808.1674401888.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga_75BBYNYN9J=GS1.1.1674633890.7.1.1674633983.0.0.0; _im_vid=01GQCX73FXBEW22BB0WVHXR401; _fbp=fb.1.1674396763223.37132445; _ga=GA1.1.1116251316.1674396762; PHPSESSID=90529190_jkIDly6jy9CkhsFWoA5kjokanoEqQkEn; a_type=0; b_type=1; c_type=22; privacy_policy_notification=0; _ga_MZ1NL4PHH0=GS1.1.1674633912.3.1.1674633965.0.0.0; device_token=aa64336f330ae88c207814dca2c5ced1; privacy_policy_agreement=5; _gid=GA1.2.235656553.1674582691; __cf_bm=ntcEyvIQ2WVI1i...feA3hEfkzTXPxTM1mm.6cqoPmc-1674633891-0-AW7ce5uvy4iTUlriU76aBrkWu2t18YePKGCF2w46sjO/KHFEUvBLZxmbl7zDDqMDn01ywUb7bCYZWqPN0o9wPBdZWPZoL/jl89JkaYxyZwxbB+p0fcTH9kO5v96OkLM2XFW1Vi7f3V1Zfmh8xpr/mQ+cu4Yk3m5AhxxfkxRsKYy1ha11LbQqNfChAVJHqAS4EuQ+fT8AYa8UJTd1W1pp5fk=; __utmt=1; tag_view_ranking=Lt-oEicbBr~RTJMXD26Ak~uW5495Nhg-~yTFlPOVybE~7ebIzNRkdM~b3tIEUsHql~Qw2RLEQgKY~jH0uD88V6F~jhuUT0OJva~EZQqoW9r8g~PEWvBxU9pH~-t_IAEknVh~RlJg_oCwwz~EmhsFxSBo-~R4YyPA5U1t~QOlvfk_Wxj~hvsnPcI8Rg~D0nMcn6oGk~_pwIgrV8TB~p76wqGJbIo~uusOs0ipBx~lKmQRiaEov~YRDwjaiLZn~5WlN6qpDZj~1HD6lhXO_A~9PI9msRK8Q~mv-jOivdpn~ZKYx1SDf_f~pnCQRVigpy~5NIG-P_d-D; cto_bundle=qGJ8Zl9uaGtIJTJCNkZISmI1ZzJVcHBsNGgzckU5YzN4WFJPRlZoN3J3RXNnUW5FOFpvbTFhJTJGZXViTWt4Qm8lMkYlMkJWYURIa3k2MGxVZFpjWFFPYU1IJTJGbURGSzBOZGxVVm9NRHJxWmNsY0wxQWpzZmlyUzEzbGlLNFRiQWc5UGFsTFpxNVIlMkZIeVhWN3djWGhQMGd6bndOSjdRajZGNlZDUDhDUGFsaDZqY0Y5ZHdIT3R0dGclM0Q; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; login_ever=yes; p_ab_d_id=702090925; p_ab_id=1; p_ab_id_2=4; first_visit_datetime_pc=2022-12-27+09%3A50%3A49; yuid_b=OWEnNRA'
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
