#!/usr/bin/env python3
#
#Парсер RSS
#import sys
#sys.path.append("/usr/local/lib/python3/dist-packages")
import feedparser
#асихронный клиент для PostgreSQL
import asyncio
import asyncpg
#official PostgreSQL client library
import psycopg2
#
import time
import datetime
#Получаем список rss-лент
conn = psycopg2.connect(dbname='webstat', user='webuser', password='!23456',  host='10.10.10.10')
cursor = conn.cursor()
cursor.execute("SELECT * FROM rss_url")
url_list = cursor.fetchall()
conn.close()

#Получаем rss
# rss[0] id
# rss[1] таблица   
# rss[2] url
# rss[3] last_etag
async def get_rss(rss):
    #Получение rss
    rssdates = feedparser.parse(rss[2], etag=rss[3])
    print ("Recive ===>", rss[1])

    if rssdates.status == 304:
        return ("no changes")

    #Запись в PostgreSQL
    conn = await asyncpg.connect(user='webuser', password='!23456', database='webstat', host='10.10.10.10')
    #Дата последней новости
    #
    last_published = await conn.fetchrow('SELECT MAX( published ) FROM ' + rss[1] + ' ;')
    #
    for item in rssdates.entries:
        #Парсим время публикации в формат MySQL
        published = datetime.datetime.strptime(item.published, "%a, %d %b %Y %H:%M:%S %z")
        if published > last_published[0]:
            await conn.execute ('INSERT INTO ' + rss[1] + ' (title, published, link) VALUES ($1, $2, $3)', item.title, published, item.link) 
        else:
            print(rss[1], published)
    #await conn.execute ('UPDATE rss_url SET etag=$1 WHERE name=$2', rssdates.etag, rss[1]) 
    print ("Insert ===>", rss[1])
    await conn.close()

async def async_get_rss():
    tasks = [asyncio.ensure_future(
        get_rss( url_list[i] )) for i in range(4, 8)]
    await asyncio.wait(tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(async_get_rss())
loop.close()



    