# OpenSearch

## Install & Run
 - Clone this repository.
 - Install all requirements via `pip install -r requirements.txt`.
 - Run the `webapp.py`.
 - Open your browser and type `http://127.0.0.1/search?q=<search keyword>`.\
 - See the following part.

## SQL preparation
 - By default, OpenSearch needs a MySQL server as a database.
 - But you can also use a SQLite server for a lite usage
 - Just replace `serve.py` by `sqlite_serve.py`.
 - But you need to add data manually
 - Also, you may remove the existing `data.db`
 - You can initialize a database via `init.sql`
 - And delete the dirty results via `delete.sql`
 - Have fun with OpenSearch!