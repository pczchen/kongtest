import elasticsearch
import urllib.request

def elastic_direct(url, method='GET', body=None, headers={}):
    
    req = res = None
    
    if body:
        req = urllib.request.Request(url,body.encode(),headers, method)
    else:
        req = urllib.request.Request(url,body,headers, method)
  
    try:
        res = urllib.request.urlopen(req)
    except urllib.request.HTTPError as e:
        print ("Failed:", url)
        print (e.code ,":", e.read())

    else:
      return res.read()

def elastic_proxy(url, method='GET', body=None, headers={}, opener=None):
    
    req = res = None
    
    if opener == None:
        proxy = urllib.request.ProxyHandler({'sock5':'localhost:8080'})
        opener = urllib.request.build_opener(proxy)
    urllib.request.install_opener(opener)
    
    if body:
        req = urllib.request.Request(url,body.encode(),headers, method)
    else:
        req = urllib.request.Request(url,body,headers, method)
  
    try:
        res = urllib.request.urlopen(req)
    except urllib.request.HTTPError as e:
        print ("Failed:", url)
        print (e.code ,":", e.read())

    else:
      return res.read()
  
def main():
    v = elastic_proxy("http://10.248.26.158:9200/_cat/indices?pretty&v")
    print(v.decode())
    
def bulk_insert(es, records=[]):    
    from elasticsearch import helpers 
    if records == None or len(records) == 0:
        record = { "_index": "chunzhi", "_type": "study", "_id": "111", "_source": 
                   { "request": "request", "response": "response"}
                 }
        records = []
        records.append(record)
    
    records.clear()
    record=[]
    import time
    for page in search_data(es):
        for r in page:
            s=r["_source"]["started_at"]
            s = time.strftime('%Y-%m-%dT%H:%M:%S.123Z',time.localtime(1466561471))
            r["_source"]["started_at"] = s
            r["_source"]["started_year"] = s[0:4]
            r["_source"]["started_month"] =s[5:7]
            r["_source"]["started_day"] = s[8:10]
            r["_source"]["started_hour"] = s[11:13]
            r["_source"]["started_minute"] = s[14:16]
            r["_source"]["started_second"] = s[17:19]            
            record={"_index": "kongtest-2016.06", "_type":"log", "_source": r["_source"]}
            records.append(record)
        
    helpers.bulk(es, records)
    
    
def search_data(es):
    page = es.search(
                     index = "kongtest-2016.06.01",
                     doc_type = "log",
                     scroll = "2m",
                     search_type = 'scan',
                     size = '100',
                     body = {  "query": { "match_all": {    }  }  }
                    )
    
    sid = page["_scroll_id"]
    total_size = page["hits"]["total"]
    while total_size > 0:
        page = es.scroll(scroll_id = sid, scroll = "2m")
        
        sid = page["_scroll_id"]
        data = page["hits"]["hits"]
        if data:
            yield data
        else:
            break
    

def handler_data():
    from datetime import datetime
    # by default we connect to localhost:9200
    es = elasticsearch.Elasticsearch()

    # datetimes will be serialized
    es.index(index="my-index", doc_type="test-type", id=42, body={"any": "data", "timestamp": datetime.now()})
    {u'_id': u'42', u'_index': u'my-index', u'_type': u'test-type', u'_version': 1, u'ok': True}

    # but not deserialized
    es.get(index="my-index", doc_type="test-type", id=42)['_source']
    {u'any': u'data', u'timestamp': u'2013-05-12T19:45:31.804229'}
    

    doc = {
        'author': 'kimchy',
        'text': 'Elasticsearch: cool. bonsai cool.',
        'timestamp': datetime.now(),
    }
    res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
    print(res['created'])
    
    res = es.get(index="test-index", doc_type='tweet', id=1)
    print(res['_source'])
    
    es.indices.refresh(index="test-index")
    
    res = es.search(index="test-index", body={"query": {"match_all": {}}})
    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
    