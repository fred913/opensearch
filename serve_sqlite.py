# coding: utf-8
# not app
# command & db only
import sqlite3
from typing import *


class Server:
    path = ""

    def __init__(self):
        self.conn = sqlite3.connect(Server.path)

    def close(self):
        self.conn.close()

    def add_url(self, title, url, description):
        print("add:", title, url, description)
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

    def search(self, orig_keywords: Iterable[AnyStr]):
        keywords = []
        for i in orig_keywords:
            if i:
                i = i.replace("[", "[[]")
                i = i.replace("_", "[_]")
                i = i.replace("%", "[%]")
                keywords.append(i)
        if len(orig_keywords) == 0:
            return []
        sent = """SELECT * FROM DATA WHERE TITLE LIKE ? OR URL LIKE ?;"""
        search_like = "%%%s%%" % (str("%".join(keywords)),)
        result = self.conn.execute(
            sent, (search_like, search_like))
        return list(result)

    def clean_url(self, url):
        while url.endswith("/"):
            url = url[:-1]
        return url
