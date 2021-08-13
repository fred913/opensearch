# coding: utf-8
# not app
# command & db only
from typing import *
import json
import requests
from serve_mysql import Server as ServeMySQL
from serve_sqlite import Server as ServeSQLite


try:
    with open("./config.json", "r", encoding="utf-8") as f:
        global config
        config = json.load(f)
except Exception:
    with open("./config.json", "w", encoding="utf-8") as f:
        json.dump({"db": {
            "sqlite": False,
            "mysql": False,
            "public": True,
            "mysql_host": "",
            "mysql_port": 3306,
            "mysql_user": "",
            "mysql_password": "",
            "mysql_database": "",
            "sqlite_path": "./data.db"
        }}, f)
    raise FileNotFoundError("Config generated. Please edit the config now")


class ServePublic:
    def __init__(self):
        self.session = requests.Session()

    def add_url(self, title, url, description):
        raise ValueError(
            "Public driver does not support add_url. Please use SQLite or MySQL")

    def url_exists(self, url):
        raise ValueError(
            "Public driver does not support url_exists. Please use SQLite or MySQL")

    def search(self, kwds):
        self.session.post("https://opensearchpublic.ft2.club/search_api")


if config["db"]['sqlite']:
    ServeSQLite.path = config["db"]['sqlite_path']
    Server = ServeSQLite
elif config["db"]['mysql']:
    ServeMySQL.host = config["db"]['mysql_host']
    ServeMySQL.port = config["db"].get('mysql_port') or 3306
    ServeMySQL.user = config["db"]['mysql_user']
    ServeMySQL.password = config["db"]['mysql_password']
    ServeMySQL.database = config["db"]['mysql_database']
    Server = ServeMySQL
elif config["db"]['public']:
    Server = ServePublic
else:
    raise ValueError("Please specify one database type")

if __name__ == "__main__":
    server = Server()
    s = input("Search: ")
    keywords = []
    for i in s.split():
        if i:
            keywords.append(i)
    print(keywords)
    result = server.search(keywords)
    print(result)
    for i in result:
        print(i)
    server.close()
