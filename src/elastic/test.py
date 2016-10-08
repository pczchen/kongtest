import elastic.base as elastic

from elasticsearch import Elasticsearch, helpers
    
es = Elasticsearch(['10.248.26.158'])

elastic.bulk_insert(es, [])

