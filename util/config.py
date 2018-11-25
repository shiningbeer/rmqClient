import ConfigParser
import sys

class Config():
    def __init__(self,file):
        try:
            config=ConfigParser.ConfigParser()
            config.read(file)
            self.rmq_host=config.get('rmq','host')
            self.rmq_user=config.get('rmq','user')
            self.rmq_password=config.get('rmq','password')
            self.cidr_task_channel=config.get('rmq','cidr_task_channel')
            self.plugin_task_channel=config.get('rmq','plugin_task_channel')
            self.cidr_result_channel=config.get('rmq','cidr_result_channel')
            self.plugin_result_channel=config.get('rmq','plugin_result_channel')
        except Exception,e:
            print u'reading config.ini error!',repr(e)
            sys.exit(0)