# not app
# command & db only
import sqlite3
from typing import *


class Server:
    def __init__(self):
        self.conn = sqlite3.connect('./data.db')

    def close(self):
        self.conn.close()

    def add_url(self, title, url, description):
        url = self.clean_url(url)
        if self.url_exists(url):
            return
        sent = """INSERT INTO DATA (ID, TITLE, URL, DESCRIPTION) 
VALUES (?, ?, ?, ?);"""
        # insert safely
        self.conn.execute(sent, (None, title, url, description))
        self.conn.commit()

    def url_exists(self, url):
        url = url.strip()
        sent = """SELECT * FROM DATA WHERE URL=?;"""
        result = self.conn.execute(sent, (url, ))
        return len(list(result)) > 0

    def search(self, keywords: Iterable[AnyStr]):
        if len(keywords) == 0:
            return []
        sent = """SELECT * FROM DATA WHERE TITLE LIKE ? OR URL LIKE ? OR DESCRIPTION LIKE ?;"""
        search_like = "%%%s%%" % (str("%".join(keywords)),)
        result = self.conn.execute(
            sent, (search_like, search_like, search_like))
        return list(result)

    def clean_url(self, url):
        while url.endswith("/"):
            url = url[:-1]
        return url


# if __name__ == "__main__":
#     server = Server()
#     server.add_url("baidu", "https://www.baidu.com/", "baidu official")
#     server.add_url("bilibili", "https://www.bilibili.com/", "bilibili")
#     print(server.search([]))
#     server.close()
