#!/usr/bin/env python3
#
#Парсер RSS
#import sys
#sys.path.append("/usr/local/lib/python3/dist-packages")
import feedparser
#асихронный клиент для PostgreSQL
import asyncio
import asyncpg

async def run():
    conn = await asyncpg.connect(user='webuser', password='!23456', database='webstat', host='10.10.10.10')
    values = await conn.fetch('''SELECT * FROM rss_lenta_ru''')
    await conn.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())

    