import requests
import re
import time
import threading

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}


def get_current_time():
    timenow = time.strftime('%Y-%m-%d %X', time.localtime())
    return timenow


def crawl():
    urls = [
        'http://www.66ip.cn/nmtq.php?getnum=600&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip']
    result = []
    for pageurl in urls:
        try:
            html = requests.get(pageurl, headers=headers, timeout=300).text
        except Exception as e:
            print('[%s][Spider][66ip]Error:' % get_current_time(), e)
            continue
        ips = re.findall('\d+\.\d+\.\d+\.\d+:\d+', html)
        result += ips
        time.sleep(2)
    print('[%s][Spider][66ip]OK!' % get_current_time(), 'Crawled IP Count:', len(result))
    return result


class SpiderIP66(threading.Thread):
    def __init__(self):
        super(SpiderIP66, self).__init__()

    def run(self):
        self.result = crawl()
