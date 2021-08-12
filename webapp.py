from serve import Server
from flask import Flask, request, redirect, jsonify, Response as FlaskResponse
app = Flask("webapp")


@app.after_request
def change_server(resp: FlaskResponse):
    resp.headers['Server'] = "OpenSearch"
    resp.headers['X-Powered-By'] = "OpenSearch"
    return resp


@app.route("/opensearch_api")
def search():
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
