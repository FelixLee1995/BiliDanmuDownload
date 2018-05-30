#!/usr/bin/python
# -*- coding: utf-8 -*-
from json import JSONDecodeError
from danmaku.utils.filePathCharFilter import filterFilepath

__author__ = "$Author: felixlee$"
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2018-05-15 15:03$"

###############################################################
# 功能：B站弹幕爬取
###############################################################
import requests
import datetime
from danmaku.utils.jsonpUtil import loads_jsonp
import json
from danmaku.object.Video import Video
from danmaku.service.upsertService import upsertAvp, upsertModifyTime, upsertAv
from danmaku.constant.constant import xmlfilepath
import os

#####################全局变量###########################################

today = datetime.datetime.today()
todayStr = datetime.datetime.strftime(today, "%Y-%m-%d")
lastDayDate = today - datetime.timedelta(1)
lastDayDateStr = datetime.datetime.strftime(lastDayDate, "%Y-%m-%d")
picname = "vdcode.png"
vdUrl = "https://account.bilibili.com/captcha"
goLoginUrl = "https://account.bilibili.com/login"
loginUrl = "https://account.bilibili.com/login/dologin"
accountUrl = "http://account.bilibili.cn/crossDomain?Expires=604800&DedeUserID=7385982&DedeUserID__ckMd5=258b1b7cb17d993c&SESSDATA=c4090d71,1450773446,55659e39&gourl=http://www.bilibili.com/"
mainUrl = "http://www.bilibili.com/"
memberUrl = "http://member.bilibili.com"
#################################################################


def getFavurl(uid):
    return 'https://space.bilibili.com/'+uid+'/#/favlist'


def getFavlist(uid):
    headers = {'Host': 'api.bilibili.com', 'Referer': 'https://space.bilibili.com/',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
    resp = requests.get('https://api.bilibili.com/x/space/fav/nav?mid=' + uid + '&jsonp=jsonp&callback=__jp7',
                        headers=headers)
    jsonstr = loads_jsonp(resp.content.decode('utf-8'))
    jsonobj = json.loads(jsonstr)
    archive = jsonobj['data']['archive']
    return archive


def convertUserlist2Userids(userlists):
    res = []
    for user in userlists:
        if user['bilimid'] not in res:
            res.append(user['bilimid'])
    return res

def getFavlistByUserids(userids):
    res = []
    for uid in userids:
        headers = {'Host': 'api.bilibili.com', 'Referer': 'https://space.bilibili.com/',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
        resp = requests.get('https://api.bilibili.com/x/space/fav/nav?mid=' + uid + '&jsonp=jsonp&callback=__jp7',
                            headers=headers)
        jsonstr = loads_jsonp(resp.content.decode('utf-8'))
        jsonobj = json.loads(jsonstr)
        archive = jsonobj['data']['archive']
        for fav in archive:
            res.append(fav)
    return res


def favlistToVideoList(archive):
    videoList = []
    for x in archive:
        if x['cur_count'] > 0:
            headers = {'Host': 'api.bilibili.com', 'Referer': 'https://space.bilibili.com/',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
            for i in range(1, int(x['cur_count']/30)+2):
                resp = requests.get('https://api.bilibili.com/x/v2/fav/video?vmid=' + str(x['mid']) + '&ps=30&fid=' + str(x['fid']) + '&tid=0&keyword=&pn=' + str(i) + '&order=fav_time&jsonp=jsonp&callback=__jp51',
                        headers=headers)
                jsonstr = loads_jsonp(resp.content.decode('utf-8'))
                jsonobj = json.loads(jsonstr)
                # print(jsonobj['data']['archives'])
                list = jsonobj['data']['archives']
                for item in list:
                    videoList.append(jsonToObject(item))
    return videoList


def favlistToAvids(archive):
    avids = []
    for x in archive:
        if x['cur_count'] > 0:
            headers = {'Host': 'api.bilibili.com', 'Referer': 'https://space.bilibili.com/',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
            for i in range(1, int(x['cur_count']/30)+2):
                resp = requests.get('https://api.bilibili.com/x/v2/fav/video?vmid=' + str(x['mid']) + '&ps=30&fid=' + str(x['fid']) + '&tid=0&keyword=&pn=' + str(i) + '&order=fav_time&jsonp=jsonp&callback=__jp51',
                        headers=headers)
                jsonstr = loads_jsonp(resp.content.decode('utf-8'))
                jsonobj = json.loads(jsonstr)
                # print(jsonobj['data']['archives'])
                list = jsonobj['data']['archives']
                for item in list:
                    if item['aid'] not in avids:
                        upsertAv(item['aid'], jsonToObject(item))
                        aidToCids(item['aid'])
                        avids.append(item['aid'])
    return avids


def jsonToObject(jsonobj):
    # res = {"aid": jsonobj['videos']}
    # return Video(jsonobj['videos'], jsonobj['title'], jsonobj['pic'], jsonobj['duration'], jsonobj['owner']['name'], jsonobj['owner']['mid'],jsonobj['owner']['face'], jsonobj['aid'])
    return {"videos": jsonobj['videos'], "title": jsonobj['title'], "pic": jsonobj['pic'], "duration": jsonobj['duration'], "ownername": jsonobj['owner']['name'], "ownerid": jsonobj['owner']['mid'], "ownerface": jsonobj['owner']['face'], "aid": jsonobj['aid']}


def aidToCids(aid):
    headers = {'Host': 'www.bilibili.com', 'Referer': 'https://space.bilibili.com/',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
    resp = requests.get('https://www.bilibili.com/video/av' + str(aid),
                        headers=headers)
    htmlStr = resp.content.decode('utf-8')
    # print(htmlStr.index('pages'))
    htmlStr1 = htmlStr[htmlStr.index('pages'):]
    try:
        avpList = json.loads(htmlStr1[htmlStr1.index('['):htmlStr1.index('}]')+2])
    except JSONDecodeError:
        print(str(aid) + "该稿件不见了！")
        # todo 日志记录
    else:
        upsertAvp(aid, avpList)



def downloadXml(avid, cid, title, page):
    print(avid)
    xml = requests.get('https://comment.bilibili.com/' + str(cid) + '.xml').content.decode('utf-8')
    dirpath = xmlfilepath + os.sep + str(avid)
    title = filterFilepath(title)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(dirpath + os.sep + 'P' + str(page) + '_' + str(title) + '.xml', 'w') as file:
        file.write(xml)
    upsertModifyTime(avid)



# archive = getFavlist('7258234')
#
# favlistToVideo(archive)

 # aidToCids("20513184")

# print(requests.get('http://comment.bilibili.com/4804674.xml').content.decode('utf-8'))

# downloadXml(3060477, 7972648,'第四十八课:行李我来拿',39)





