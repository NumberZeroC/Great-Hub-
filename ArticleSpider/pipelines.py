# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


#一般方法连接Mysql
class MysqlPipeline():
    def __init__(self):
        self.conn = pymysql.connect(host='localhost',user='root', passwd='password', db='pipline',port=3306,
                                    charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into comment(name,title,star,date,movie_name,text,support,oppose,img_url,movie_url)
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(
            item['name'], item['title'], item['star'], item['date'], item['movie_name'],
            item['text'], item['support'], item['oppose'], item['img_url'], item['movie_url'],
        ))
        self.conn.commit()


# 异步IO写入mysql
# class MysqlTwistedPipline():
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, settings):
#         dbparms = dict(
#             host=settings['MYSQL_HOST'],
#             db=settings['MYSQL_DB'],
#             user=settings['MYSQL_USER'],
#             passwd=settings['MYSQL_PASSWORD'],
#             charset='utf8',
#             port=3306
#
#         )
#         dbpool = adbapi.ConnectionPool('pymysql',dbparms)
#         return cls(dbpool)
#
#     def process_item(self, item, spider):
#         query = self.dbpool.runInteraction(self.do_insert, item)
#         query.addErrorback(self.handle_error)
#
#     def handle_error(self, failure):
#         print(failure)
#
#     def do_insert(self,cursor,item):
#         insert_sql = """
#                     insert into comment(name,title,star,date,movie_name,text,support,oppose,img_url,movie_url)
#                     values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#                 """
#         cursor.execute(insert_sql, (
#             item['name'], item['title'], item['star'], item['date'], item['movie_name'],
#             item['text'], item['support'], item['oppose'], item['img_url'], item['movie_url'],
#         ))





















