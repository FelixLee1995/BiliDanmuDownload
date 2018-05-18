import time
from pymongo import MongoClient

client = MongoClient()
danmaku = client.danmaku


def upsertAvp(avid,avpList):
    nowtime= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    res = danmaku.av.update({"avid": avid}, {"$set": {"avplist": avpList, "createTime": nowtime}}, upsert=True)
    return res

def upsertAv(avid,avitem):
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    res = danmaku.av.update({"avid": avid}, {"$set": {"avinfo": avitem, "createTime": nowtime}}, upsert=True)
    return res

def upsertModifyTime(avid):
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    res = danmaku.av.update({"avid": avid}, {"$set": {"syncTime": nowtime}}, upsert=True)


