# OpenSearch

## 安装 & 运行
 - 1、克隆这个仓库.
 - 2、安装必要扩展 `pip install -r requirements.txt`.
 - 3、运行这个文件 `webapp.py`.
 - 4、打开你的浏览器并输入 `http://127.0.0.1/search-result-page?q=<关键词>`.\
 - 5、查看下面一个小节以初始化你的数据库。

## SQL 初始化
 - 默认情况下, OpenSearch 需要一个MySQL服务器作为数据库.
 - 当然，如果你只需要自己使用一下，或是临时性/小规模的部署
 - 你也可以使用SQLite版本的`serve.py`
 - 只需要用`sqlite_serve.py`替换`serve.py`
 - <small>注：不过我们在测试时，SQLite未能识别`import.sql`中的一些语法，你需要自行调试（雾</small>
 - 你可以删除现有的`data.db`，并自行创建新的数据库
 - 请使用`init.sql`初始化一个**新的**数据库（SQLite直接使用，MySQL还需要增加`AUTO_INCREMENT`标签）
 - `delete.sql`也可以用于删除一些冗余/无用的数据
 - 现在去玩玩OpenSearch吧🤣
 - 另外，我们也提前爬取好了一大堆数据。直接导入`import.sql`，有一个10000+数据的大礼包等着你😁