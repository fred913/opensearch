from serve import Server
import requests
import html_parser
from bs4 import BeautifulSoup
import queue


def refactor_url(parent, uri):
    uri = uri.split("#")[0]
    parent = parent.split("#")[0]
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
    url = url.split("#")[0]
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
server.close()
server = Server()

# bs=bs4.BeautifulSoup()

starter = input("Start from?")
tasks = queue.Queue(maxsize=300)
tasks.put((starter, 0))
while True:
    try:
        print("还剩%d个url" % (tasks.qsize(),))
        try:
            url, level = tasks.get(block=False)
            if level > 4:
                print("level too high; continue")
                continue
        except queue.Empty:
            print("All finished. exiting...")
            break
        print("parse url (level %d):" % (level,), url)
        try:
            response = requests.get(url, headers={
                "User-Agent": "OpenSearchSpider/1.0"
            }, timeout=0.8)
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
        title = soup.title.string if soup.title else "未找到标题"
        try:
            description = soup.select("meta[name=description]")[0].attrs['content']
        except:
            description = "无法获取此页的描述。"
        server.add_url(title=title, url=url, description=description)
        for i in soup.select("a[href]"):
            if len(i.attrs.get('href')) > 90:
                continue
            if i.attrs.get('href'):
                sub_url.add(clean_url(i.attrs.get('href')))
        for i in sub_url:
            try:
                if "mailto:" in i:
                    continue
                tasks.put((refactor_url(url, i), level+1), block=False)
            except queue.Full:
                continue
    except KeyboardInterrupt:
        print("Exiting...")
        break
server.close()
