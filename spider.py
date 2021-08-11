from serve import Server
import requests
import html_parser
from bs4 import BeautifulSoup
import queue


def refactor_url(parent, uri):
    if uri.startswith("http://") or uri.startswith("https://"):
        return uri
    if uri.startswith("//"):
        return parent.split("//")[0] + uri
    if not uri.startswith("/"):
        return "/".join(parent.split("/")[:-1]) + "/" + uri
    else:
        a = "%s//%s%s" % (parent.split("//")[0], parent.split("/")[2], uri)
        return a

def clean_url(url):
    while url.endswith("/"):
        url = url[:-1]
    return url


def auto_encoding(b: bytes):
    try:
        b.decode("utf-8")
        return "utf-8"
    except Exception:
        try:
            b.decode("gb2312")
            return "gb2312"
        except Exception:
            try:
                b.decode("gbk")
                return "gbk"
            except Exception:
                return None


session = requests.Session()
server = Server()
# bs=bs4.BeautifulSoup()

starter = input("Start from?")
tasks = queue.Queue()
tasks.put(starter)
while True:
    print("还剩%d个url" % (len(tasks),))
    try:
        sub_url = tasks.get(block=False)
    except queue.Empty:
        print("All finished. exiting...")
        break
    print("parse url:", sub_url)
    try:
        response = requests.get(sub_url, headers={
            "User-Agent": "OpenSearchSpider/1.0"
        })
        assert response.status_code == 200
    except Exception:
        print("get url error. continue...")
        continue
    response.encoding = auto_encoding(response.content)
    sub_url = set()
    for i in html_parser.re_get_url_list(response.text):
        if len(i) > 90:
            continue
        sub_url.add(clean_url(i))
    soup = BeautifulSoup(response.text, "lxml")
    title = soup.title.string
    try:
        content = soup.select("meta[name=description]")[0].attrs['content']
    except:
        content = "无法获取此页的描述。"
    for i in soup.select("a[href]"):
        if len(i.href) > 90:
            continue
        if i.attrs.get('href'):
            sub_url.add(clean_url(i.attrs.get('href')))
    for i in sub_url:
        tasks.put(i)
