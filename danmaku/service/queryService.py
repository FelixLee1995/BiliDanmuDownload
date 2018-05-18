from pymongo import MongoClient
import time

client = MongoClient()
danmaku = client.danmaku


def findUserTobeScan():
    userids = []
    for user in danmaku.user.find({'scanSync': '0'}):
        userids.append(user)
    return userids


def findAvIfExists(avid):
    return danmaku.av.find_one({'avid': avid}, {'avplist': 1})


def findCinfosByAvid(avid):
    cinfos = []
    # res = danmaku.av.find_one({'avid': avid})
    # print(res)
    for av in danmaku.av.find({'avid': avid}):
        if 'avplist' in av:
            av = av['avplist']
            for x in av:
                if 'cid' in x:
                    info = {'cid': x['cid'], 'page': x['page'], 'title': x['part']}
                    cinfos.append(info)
    return cinfos

def filterNeedDownloadAvlist(avlist):
    nowtime = time.mktime(time.localtime())
    filter = []
    for avid in avlist:
        print(avid)
        x= danmaku.av.find_one({'avid': avid})
        if 'syncTime' in x:
            synctime = time.mktime(time.strptime(x['syncTime'], '%Y-%m-%d %H:%M:%S'))
            if (nowtime - synctime) < 60 * 60 * 24:
                filter.append(avid)
    for x in filter:
        avlist.remove(x)
    print(avlist)
    return avlist


# nowtime = time.mktime(time.localtime())
# for x in danmaku.av.find({'avid': 1639335}):
#     print(x)
#     if 'syncTime' in x:
#         synctime = time.mktime(time.strptime(x['syncTime'], '%Y-%m-%d %H:%M:%S'))
#         print(nowtime-synctime)

#filterNeedDownloadAvlist([1639335])

# print(danmaku.av.find_one({'avid': 1639335}))