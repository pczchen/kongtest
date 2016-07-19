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
    
def bulk_insert(es=None, records=[]):
    from elasticsearch import Elasticsearch, helpers
    
    if es == None:
        es = Elasticsearch(['10.248.26.158'])
        
    if records == None or len(records) == 0:
        record = { "_index": "chunzhi", "_type": "study", "_id": "111", "_source": 
                   { "request": "request", "response": "response"}
                 }
        records = []
        records.append(record)
    helpers.bulk(es, records)
    
def search_data(es):
    page = es.search(
                     index = "chunzhi",
                     doc_type = "type",
                     scroll = "2m",
                     search_type = 'scan',
                     size = 1000,
                     body = {  "query": { "match_all": {    }  }  })
    
    sid = page["_scroll_id"]
    scroll_size = page["hits"]["total"]
    
    while scroll_size > 0:
        page = es.scroll(scroll_id = sid, scroll = "2m")
        
        sid = page["_scroll_id"]
        scroll_size = page["hits"]["total"]
    

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
    