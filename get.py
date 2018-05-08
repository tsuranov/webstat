#!/usr/bin/env python3
#
#Парсер RSS
#import sys
#sys.path.append("/usr/local/lib/python3/dist-packages")
import feedparser
#Клиент для PostgreSQL
import asyncio
import asyncpg

async def run():
    conn = await asyncpg.connect(user='webuser', password='!23456', database='webstat', host='10.10.10.10')
    values = await conn.fetch('''SELECT * FROM rss_lenta_ru''')
    await conn.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())

#print ("Start read RSS Lenta.ru")
#url = 'https://lenta.ru/rss'
#rssdates = feedparser.parse(url)

#print (rssdates.modified_parsed)
#print (rssdates.etag)
#last_etag = rssdates.etag

#rssdates = feedparser.parse(url, etag=last_etag)
#if rssdates.status == 304:
#    print ("no changes")


#print (rssdates.version)
#print (d.feed.title)
#print (d.feed.link)
#print (d.feed.description)

#print (len(d.entries))

#for item in d.entries:
#    print ("-----------------------------------", "\n")
#    print (item.title, "\n", item.title_detail.value, "\n")
#    print ("##########################", "\n")
#    print (item.summary, "\n")
#    print ("##########################", "\n")
#    print (item.summary_detail.value, "\n")
#    print ("##########################", "\n")
#    print (item.published)
#    print ("##########################", "\n")
#    print (item.link)



    