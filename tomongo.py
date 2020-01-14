import pymongo
import json

# 1.连接本地数据库服务
connection = pymongo.MongoClient('localhost')
# 2.连接本地数据库 demo。没有会创建
db = connection.movie
# 3.创建集合
emp = db.tags
# 根据情况清空所有数据
emp.remove(None)

# 4.打开外部文件
file = open('D:\wrjk-spider-master\movie.json', 'r', encoding="utf-8")
for each in file:
    eachline = json.loads(each)
    emp.insert(eachline)
file.close()
