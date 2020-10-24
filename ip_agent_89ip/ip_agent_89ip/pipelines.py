# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from twisted.enterprise import adbapi
from pymysql import cursors
class IpAgent89IpPipeline:
   def __init__(self):
       dbparams={
           'host': '127.0.0.1',
           'port': 3306,
           'user': 'root',
           'password': '123456',
           'database': 'zz',
           'charset': 'utf8',
           'cursorclass': cursors.DictCursor
       }
       self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
       self._sql = None


   #定义插入语句
   @property
   def sql(self):
       if not self._sql:
           self._sql = """
                   insert into ip_list_all (ip_url, port, perators, recording_time)  value (%s,%s,%s,%s)
                   """
           return self._sql
       return self._sql


   def process_item(self, item, spider):
       # 对sql语句进行处理
       defer = self.dbpool.runInteraction(self.insert_item, item)  # 执行函数insert_item 去插入数据
       defer.addErrback(self.handle_error, item, spider)  # 遇到错误信息调用 handle_error方法

   def insert_item(self, cursor, item):
       cursor.execute(self.sql, (
           item['ip_url'],
           item['port'],
           item['perators'],
           item['recording_time']
       ))

   def handle_error(self, error, item, spider):
       print('*' * 20 + 'error' + '=' * 20)
       print(error)
       print('*' * 20 + 'error' + '*' * 20)
