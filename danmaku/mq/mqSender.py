import pika
from danmaku.service.queryService import findCinfosByAvid


def sendDownloadXmlMsg(avid):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='downloadxml')

    cinfos = findCinfosByAvid(avid)
    print(cinfos)
    for info in cinfos:
        args = {'avid': avid, 'cid': info['cid'], 'title': info['title'], 'page': info['page']}
        channel.basic_publish(exchange='',
                              routing_key='downloadxml',
                              body=str(args))
        print("send msg to queue [downloadxml] avid " + str(avid) + " cid " + str(info['cid']))
    connection.close()

# sendDownloadXmlMsg(16726363)
