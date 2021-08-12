# coding: utf-8
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


def auto_encoding(b: bytes, ltry: str = None):
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
                try:
                    b.decode(ltry)
                    return ltry
                except Exception:
                    return None


session = requests.Session()
server = Server()
server.close()
server = Server()

# bs=bs4.BeautifulSoup()

starter = input("Start from?")
tasks = queue.Queue()
tasks.put(starter)
while True:
    try:
        print("还剩%d个url" % (tasks.qsize(),))
        try:
            url = tasks.get(block=False)
        except queue.Empty:
            print("All finished. exiting...")
            break
        print("parse url:", url)
        try:
            response = session.get(url, headers={
                "User-Agent": "OpenSearchSpider/1.0",
                "Upgrade-Insecure-Requests": "1"
            }, timeout=1, stream=True)
            if response.headers.get("content-type").startswith("text/"):
                response_text = response.content
            else:
                print("Wrong content type:",
                      response.headers.get("content-type"))
                continue
            assert response.status_code == 200
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.InvalidURL:
            continue
        except AssertionError:
            continue
        except Exception:
            print("get url error. continue...")
            import traceback
            # traceback.print_exc()
            continue
        encoding = auto_encoding(response_text)
        if encoding is None:
            print("binary; skipping")
            continue
        else:
            print("encoding:", encoding)
        response_text = response_text.decode(encoding)
        # print(response_text)
        sub_url = set()
        for i in html_parser.re_get_url_list(response_text):
            if len(i) > 90:
                continue
            sub_url.add(clean_url(i))
        soup = BeautifulSoup(response_text, "lxml")
        title = soup.title.string if soup.title else None
        if title is None:
            continue
        try:
            description = soup.select("meta[name=description]")[
                0].attrs['content']
        except:
            description = "无法获取此页的描述。"
        if not server.url_exists(url):
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
                if "javascript:" in i:
                    continue
                i_noparam = i.split("?")[0]
                if i_noparam.endswith(".jpg"):
                    continue
                if i_noparam.endswith(".gif"):
                    continue
                if i_noparam.endswith(".png"):
                    continue
                if i_noparam.endswith(".zip"):
                    continue
                if i_noparam.endswith(".ico"):
                    continue
                if i_noparam.endswith(".js"):
                    continue
                if i_noparam.endswith(".css"):
                    continue
                if i_noparam.endswith(".svg"):
                    continue
                if i_noparam.endswith(".webp"):
                    continue
                if i_noparam.endswith("ajax.php"):
                    continue
                if i.startswith("https://bbs.yhdzz.cn/oauth/"):
                    continue
                if i.startswith("http://wpa.qq.com/msgrd"):
                    continue
                if "cnzz.com/z_stat.php" in i:
                    continue
                if "/login" in i or "/user-sign" in i:
                    continue
                # if not server.url_exists(clean_url(refactor_url(url, i))):
                tasks.put(
                    (refactor_url(url, i)), block=False)

            except queue.Full:
                continue
    except KeyboardInterrupt:
        print("Exiting...")
        break
server.close()
