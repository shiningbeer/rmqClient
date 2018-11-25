#!/usr/bin/env python
from util.sender import Sender
from util.logger import logger
from util.receiver import Receiver
import json
from time import sleep
import ConfigParser
config=ConfigParser.ConfigParser()
config.read('config.ini')
host=config.get('rmq','host')
receive_channel=config.get('rmq','plugin_task_channel')
result_channel=config.get('rmq','plugin_result_channel')

send=Sender(host,result_channel)

def getScanFunc(plugin):

    try:
        exec("from plugins import " + plugin + " as scanning_plugin")
    except Exception, e:
        print str(e)
        return None
    return scanning_plugin.scan

def deal_with_msg(body):
    try:
        task=json.loads(body)    
        id=task['_id']
    except Exception, e:
        logger.error(repr(e))
        tr={'error':repr(e)}
        trstr=json.dumps(tr)
        send.send_msg(trstr)
        return
    try:
        port=task['port']
        ip=task['ip']
        plugin=task['plugin']
        scan=getScanFunc(plugin)
    except Exception,e:
        logger.error(repr(e))
        tr={'_id':id,'error':repr(e)}
        trstr=json.dumps(tr)
        send.send_msg(trstr)
        return

    logger.info("Received %r" % task['_id'])
    result=scan(ip,port)
    tr={'_id':task["_id"],'result':result}
    trstr=json.dumps(tr)
    send.send_msg(trstr)

receive=Receiver(host,receive_channel,deal_with_msg)
receive.start_listen()