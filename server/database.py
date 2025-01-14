from elasticsearch import Elasticsearch
import time
from dotenv import load_dotenv, dotenv_values

load_dotenv()

DB_HOST = dotenv_values('.env').get('DB_HOST')

es = Elasticsearch([{'host': DB_HOST, 'port': 9200, 'scheme': 'http'}])

while not es.ping():
    print("Fail on Elasticsearch connect! Retrying...")
    time.sleep(5)

print("Successfully connected to Elasticsearch!")