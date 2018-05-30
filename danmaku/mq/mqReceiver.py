import pika
from danmaku.web.access import downloadXml

def receiveDownloadXmlMsg():
    pika.ConnectionParameters(blocked_connection_timeout=400)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='downloadxml')

    def callback(ch, method, properties, body):
        argsdict = eval(body.decode('utf-8'))
        print(" [x] Received %r" % body.decode('utf-8'))
        downloadXml(argsdict['avid'], argsdict['cid'], argsdict['title'], argsdict['page'])

    channel.basic_consume(callback,
                          queue='downloadxml',
                          no_ack=True)

    print(' [*] Waiting for DownloadXml messages.')
    channel.start_consuming()


receiveDownloadXmlMsg()


