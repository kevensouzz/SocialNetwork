from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

if not es.ping():
    print("Fail on Elasticsearch connect!")
