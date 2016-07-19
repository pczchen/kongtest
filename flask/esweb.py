from flask import Flask,url_for,request,render_template

app = Flask(__name__)

@app.route("/index", methods=['GET','POST'])
def index():
    if request.method == 'GET':
       return "this is a index page"
    else:
       return "that is a index page"

@app.route("/hello")
def hello():
    return "Hello world"

@app.route("/hi/<username>")
def hi(username):
    return "Hello: %s" % username

@app.route("/")
def default():
    urls=[]
    urls.append({"name":"testindex", "url": url_for("index")})
    urls.append({"name":"testhello", "url": url_for("hello")})
    urls.append({"name":"testhi", "url": url_for("hi",username="chunzhi")})
    urls.append({"name":"teststatic","url": url_for("static",filename="logo1.jpg")})

    urls.append({"name":"Elastic stat", "url": url_for("es_stat")})
    urls.append({"name":"Kong API stat", "url": url_for("api_stat")})
    urls.append({"name":"remote es stat","url": url_for("es_stattest")})  
      
    return render_template("default.html", urls=urls)

@app.route("/elastic")
def es_stat():
    import elastic.base as es
    import re
    
    regx = re.compile("\s+")
    
    v = es.elastic_proxy("http://10.248.26.158:9200/_cat/indices?pretty&v")
    v = v.decode().strip()
    table=[]
    first = True
    for line in v.split("\n"):
        line = line.strip()
        if first:
            h = regx.split(line)
            first = False
        else:
            f = regx.split(line)
            table.append(dict(zip(h,f)))
    table.sort(key=lambda x: x["index"])
    
    table= filter(lambda x: x["index"].startswith("kongtest"),table)
    return render_template("es_stat.html",table=table)

@app.route("/apistats")
def api_stat():
    import elastic.base as es
    import re
    import json
    
    regx = re.compile("\s+")
    
    body = '''{"aggs":{"kong_api":{"terms": {"field": "api.name" },"aggs": {
        "latencies.request": {"avg": {"field": "latencies.request"}},
        "latencies.kong": {"avg": {"field": "latencies.kong" }},
        "latencies.proxy": {"avg": {"field": "latencies.proxy" }},
        "latencies.request.max": {"max": {"field": "latencies.request" }},
        "latencies.kong.max": {"max": {"field": "latencies.kong"  }},
        "latencies.proxy.max": {"max": {"field": "latencies.proxy" }},
        "last.access.time": {"max": {"field": "started_at" }}
    }}}}'''
    
    v = es.elastic_proxy("http://10.248.26.158:9200/kongtest*/_search?search_type=count",body=body)
    v = v.decode().strip()
    v = json.loads(v)

    buckets = v["aggregations"]["kong_api"]["buckets"]
    buckets.reverse()
    
    for bb in buckets:
        vv = bb["last.access.time"]["value"]
        import time
        vv = time.localtime(vv/1000)
        bb["last.access.time"]["value"] = time.strftime("%Y.%m.%d %H:%M:%S ",vv) 
    
    return render_template("api_stat.html",table=buckets)

@app.route("/elastic_test")
def es_stattest():
    import elastic.base as es
    import re
    
    regx = re.compile("\s+")
    
    v = es.elastic_direct("http://10.248.26.51:9200/_cat/indices?pretty&v")
    v = v.decode().strip()
    table=[]
    first = True
    for line in v.split("\n"):
        line = line.strip()
        if first:
            h = regx.split(line)
            first = False
        else:
            f = regx.split(line)
            table.append(dict(zip(h,f)))
    table.sort(key=lambda x: x["index"])
    
    return render_template("es_stat.html",table=table)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
    
