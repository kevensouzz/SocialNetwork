from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

if es.ping():
    print("Elasticsearch is running!")
else:
    print("Fail on Elasticsearch connect.")