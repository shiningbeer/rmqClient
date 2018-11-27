# -*- coding:utf-8 -*-
from abc import ABCMeta, abstractmethod
from pymongo import MongoClient as mc
import pymongo
import datetime
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class Dao(object):
    # 构造时连接数据库
    def __init__(self,host, port,db_name):
        try:
            self.client = mc(host,port)
            # self.client = mc('mongodb://192.168.3.123:27017')
            self.client.admin.command('ismaster')
            self.db = self.client[db_name]
        except Exception,e:
            print u'cannot connect database!',repr(e)
            sys.exit(0)
    def update_many(self,col,find_dict,update_dict):
        coll=self.db[col]
        return coll.update_many(find_dict, {"$set":update_dict })

    def update_one(self,col,find_dict,update_dict):
        coll=self.db[col]
        return coll.update_one(find_dict, {"$set":update_dict })
    def find_one(self,col,find_dict):
        coll=self.db[col]
        return coll.find_one(find_dict)
    def find_many(self,col,find_dict):
        coll=self.db[col]
        return coll.find(find_dict)
    def find_count(self,col,find_dict):
        coll=self.db[col]
        return coll.find(find_dict).count()

    def insert_one(self,tableName,document):
        coll=self.db[tableName]
        return coll.insert_one(document).inserted_id
    def delete_many(self,tname,find_dict):
        coll=self.db[tname]
        return coll.delete_many(find_dict)
    def delete_one(self,tname,find_dict):
        coll=self.db[tname]
        return coll.delete_one(find_dict)
    def drop_col(self,tname):
        return self.db.drop_collection(tname) 

    def find_one_and_update(self,tname,find_dict,update_dict):
        coll=self.db[tname]
        return coll.find_one_and_update(find_dict,{"$set":update_dict})
    def list_collection_names(self):
        return self.db.list_collection_names()
    def collection_exits(self,col):
        cols=self.db.list_collection_names()
        return col in cols

if __name__ == '__main__':
    dbo=Dao('localhost',27017,'cidrTask')
    dbo.drop_col('ii')
    # print dbo.list_collection_names()
    # print dbo.collection_exits('use')
    # dbo.insert('task',{'ipv4':{'name':'s7.py'},'ipRange':['210.203.0.1','210.203.0.1','202,21.1.1'],'paused':False,'complete':False,'goWrong':False,'running':False,'progress':0,'type':'ipv4'})
