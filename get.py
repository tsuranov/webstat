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
    if rssdates.status == 304:
        return ("no changes")

    #Запись в PostgreSQL
    conn = await asyncpg.connect(user='webuser', password='!23456', database='webstat', host='10.10.10.10')
    for item in rssdates.entries:
        values = await conn.execute ("INSERT INTO $1 (title, summary, published, link) VALUES ($2, $3, $4)", 
            rss[1], item.title, item.summary, item.published, item.link) 
    await conn.close()

async def async_get_rss():
    tasks = [asyncio.ensure_future(
        get_rss( url_list[i] )) for i in range(0, 1)]
    await asyncio.wait(tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(async_get_rss())
loop.close()



    