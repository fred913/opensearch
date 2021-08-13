# OpenSearch

## 安装 & 运行
 - 1、克隆这个仓库.
 - 2、安装必要扩展 `pip install -r requirements.txt`.
 - 3、运行这个文件 `webapp.py`.
 - 4、打开你的浏览器并输入 `http://127.0.0.1/search-result-page?q=<关键词>`.\
 - 5、查看下面一个小节以初始化你的数据库。

## SQL 初始化
 - By default, OpenSearch accesses the public sql to get data.
 - But you can configure your-own sql server - 
    just edit `config.json` (generated after running `serve.py`)