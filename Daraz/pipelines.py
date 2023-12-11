# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
# import psycopg2

class DarazPipeline:
    
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        #for mysql mysql.connector,connect is used and psycopg2 for postgre
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            #for mysql passwd is used instead of proper spellings
            passwd='tsatsatsa9',
            database='mysqldata',

        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute(""" DROP TABLE IF EXISTS mydata_tb""")
        self.curr.execute("""create table mydata_tb(
            product_name text,
            product_price text
        )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):

        self.curr.execute(""" insert into mydata_tb values(%s,%s)""", (
            item['product_name'],
            item['product_price']
        ))
        self.conn.commit()
