import schedule
import pika
import time
import danmaku.service.queryService as danmakuQueryService
import danmaku.web.access as access
from danmaku.mq.mqSender import sendDownloadXmlMsg


def job():
    print('begin ScanUserJob at ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    users = danmakuQueryService.findUserTobeScan()
    userids = access.convertUserlist2Userids(users)
    favlists = access.getFavlistByUserids(userids)
    avlist = danmakuQueryService.filterNeedDownloadAvlist(access.favlistToAvids(favlists))

    for avid in avlist:
        sendDownloadXmlMsg(avid)

#
# def keepRabbitMqConnectionAlive():
#     connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
#     pika.ConnectionParameters(blocked_connection_timeout=200)
#     connection.process_data_events()



# schedule.every(30).seconds.do(keepRabbitMqConnectionAlive)


# while True:
#     schedule.run_pending()
#     time.sleep(1)


job()