import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
client = pymongo.MongoCLient('mongodb://localhost:27017/')

"""---------------------指定数据库------------------------"""
db = client['test']
db = client.test

"""---------------------指定collection------------------------"""
collection = db['test']
collection = db.test

"""---------------------插入数据------------------------"""
student1 = {
    "id": "20240901",
    "name": "dingao",
    "age": 20,
    "gender": "male",
}

student2 = {
    "id": "20240901",
    "name": "Tom",
    "age": 25,
    "gender": "male",
}
result = collection.insert_one(student1)
result = collection.insert_many([student1,student2])
print(result)
print(result.inserted_id)

"""---------------------查询------------------------"""
result = collection.find_one({'name': 'dingao'})
result = collection.find({'name': 'dingao'})
for i in result:
    print(i)
print(type(result))  #<class 'dict'>
print(result)

"""---------------------比较运算符------------------------"""
rules = ['gt','gte','lt','lte','ne','in','nin']
results = collection.find({'age':{"$gt":25}})

"""---------------------计数------------------------"""
count = collection.find().count()
print(count)

"""---------------------排序------------------------"""
results = collection.find().sort("name", pymongo.ASCENDING) #pymongo.DESCENDING
print([result['name'] for result in results])

"""---------------------偏移(大偏移量慎用)------------------------"""
results = collection.find().skip(1)
print([result['name'] for result in results])

from bson.objectid import ObjectId
collection.find({'_id': ObjectId('66d24afe4e1e18f5eced89cc')})

"""---------------------update------------------------"""
condition = {'name':'dingao'}
student = collection.find_one(condition)
student['age'] = 25
result = collection.update_one(condition, {'$set': student})
print(result)
print(result.matched_count,result.modified_count)

condition = {'age':{'$gt':20}}
result = collection.update_one(condition, {'$inc':{'age':1}})
print(result)
print(result.matched_count, result.modified_count)

"""---------------------delete------------------------"""
result = collection.delete_many({'name':'dingao'})
print(result.deleted_count)
