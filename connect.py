import pymongo

# connect ke lokal
client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client['db_kemiskinan']

collection = db['data_statistik']