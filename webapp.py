from serve import Server
from flask import Flask, request, redirect, jsonify, Response as FlaskResponse, render_template
app = Flask("webapp")


@app.after_request
def change_server(resp: FlaskResponse):
    resp.headers['Server'] = "OpenSearch"
    resp.headers['X-Powered-By'] = "OpenSearch"
    return resp


@app.route("/search")
def search_page():
    word = request.args.get("q")
    result = search(word)
    return render_template("search.html", word=word, result=result, result_count=len(result))


def search(word):
    server = Server()
    if not word:
        return []
    kw = []
    for i in word.strip().split():
        if not i:
            continue
        kw.append(i)
    if len(kw) == 0:
        return []
    result = server.search(kw)
    server.close()
    return result


@app.route("/opensearch_api")
def webapi_search():
    server = Server()
    word = request.args.get("q")
    if not word:
        return redirect("/")
    kw = []
    for i in word.strip().split():
        if not i:
            continue
        kw.append(i)
    if len(kw) == 0:
        return []
    result = server.search(kw)
    server.close()
    return jsonify(result)


if __name__ == "__main__":
    try:
        app.run("0.0.0.0", 80, debug=False, threaded=True)
    except KeyboardInterrupt:
        pass
