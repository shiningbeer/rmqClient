#!/usr/bin/env python
from util.sender import Sender
from util.logger import logger
from util.config import Config
from util.receiver import Receiver
import json
import os
from threading import Thread
from time import sleep
import sys
from importlib import import_module
config=Config('./util/config.ini')

try:
    if len(sys.argv)==1:
        run_count=1
    else:
        run_count=int(sys.argv[1])
except Exception,e:
    print u'sys args wrong!',repr(e)
    sys.exit(0)

def send_result(name,id,msg):
    tr={'name':name,'_id':id,'msg':msg}
    trstr=json.dumps(tr)
    while True:
        try:
            send=Sender(config.rmq_host,config.rmq_user,config.rmq_password,config.ipv4_result_channel)
            send.send_msg(trstr)
            send.close()
        except Exception,e:
            print u'cannot connect rmq server!',repr(e)
            sleep(3)
            continue
        break
def deal_with_msg(body):
    try:
        task=json.loads(body)    
        id=task['_id']
        ip=task['ip']
        port=task['port']
        name=task['name']
        plugin=task['plugin']
    except Exception, e:
        logger.error(repr(e))
        msg={'error':repr(e),'originalMsg':body}
        send_result(None,None,msg)
        return
    print ("Received %r" % id)
    try:
        result=import_module('plugins.'+plugin).scan(ip,port)
    except Exception, e:
        print str(e)
        logger.error(repr(e))

        msg={'error':repr(e)}
        send_result(name,id,msg)
        return
    if result==None or result=={}:
        msg={'result':None}
    msg={'result':result}
    send_result(name,id,msg)
# to do: if temp_file still exist, it means that the result has not been sent, deal with that

for i in range (run_count):
    receive=Receiver(config.rmq_host,config.rmq_user,config.rmq_password,config.ipv4_task_channel,deal_with_msg)
    t=Thread(target=receive.start_listen).start()