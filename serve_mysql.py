import sqlite3
from typing import *
import MySQLdb
import json


class Server:
    host: str = ""
    port: int = 3306
    user: str = ""
    password: str = ""
    database: str = ""

    def __init__(self):
        self.conn = MySQLdb.connect(
            host=Server.host, port=Server.port, database=Server.database, user=Server.user, password=Server.password, charset='utf8')

    def close(self):
        self.conn.close()

    def add_url(self, title, url, description):
        print("add:", title, url, description)
        url = self.clean_url(url)
        if self.url_exists(url):
            return
        sent = """INSERT INTO DATA (ID, TITLE, URL, DESCRIPTION) 
VALUES (%s, %s, %s, %s);"""
        # insert safely
        cursor = self.conn.cursor()
        cursor.execute(sent, (None, title, url, description))
        self.conn.commit()

    def url_exists(self, url):
        url = url.strip()
        sent = """SELECT * FROM DATA WHERE URL=%s;"""
        cursor = self.conn.cursor()
        try:
            cursor.execute(sent, (url, ))
        except MySQLdb._exceptions.OperationalError:
            self.conn = MySQLdb.connect(
                mysql_config.HOST, mysql_config.USER, mysql_config.PASSWORD, mysql_config.DATABASE, charset='utf8')
            cursor = self.conn.cursor()
            cursor.execute(sent, (url, ))
        result = cursor.fetchall()
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
        sent = """SELECT * FROM DATA WHERE TITLE LIKE %s OR URL LIKE %s;"""
        search_like = "%%%s%%" % (str("%".join(keywords)),)
        # print(search_like)
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                sent, (search_like, search_like))
        except MySQLdb._exceptions.OperationalError:
            self.conn = MySQLdb.connect(
                mysql_config.HOST, mysql_config.USER, mysql_config.PASSWORD, mysql_config.DATABASE, charset='utf8')
            cursor = self.conn.cursor()
            cursor.execute(
                sent, (search_like, search_like))
        result = cursor.fetchall()
        return list(result)

    def clean_url(self, url):
        while url.endswith("/"):
            url = url[:-1]
        return url
