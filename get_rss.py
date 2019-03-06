#!/usr/bin/env python3
######################################################################
#Получение RSS
#Загрузка RSS
######################################################################
#import sys
#sys.path.append("/usr/local/lib/python3/dist-packages")
import time
import datetime
#скачивание rss-лент
import feedparser
#асихронный клиент для PostgreSQL
import asyncio
import asyncpg
#official PostgreSQL client library
#import psycopg2

#Логирование работы
# https://docs.python.org/3/howto/logging.html
import logging


async def get_rss():
    try:
        logger = logging.getLogger("get_rss")
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler("get_rss.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.info("Start get_rss()")
        
        con = await asyncpg.connect(user='webuser', password='!23456', database='webstat', host='10.10.10.10')
        #Получаем список rss-лент
        # rss[0] id
        # rss[1] таблица   
        # rss[2] url
        # rss[3] last_etag
        url_list = await con.fetch('''SELECT * FROM rss_url;''')
        logger.info("List url rss recived")

        for rss in url_list:
            #print ("Get rss: " + rss[1])
            rssdates = feedparser.parse(rss[2], etag=rss[3])
            logger.info("Recive rss: " + rss[1])

            if rssdates.status == 304:
                return ("no changes")

            #Дата последней новости в БД
            last_published = (await con.fetchrow('''SELECT MAX( published ) FROM ''' + rss[1] + ''' ;'''))[0]

            #
            i = 0
            for item in rssdates.entries:
                #Парсим время публикации в формат MySQL
                published = datetime.datetime.strptime(item.published, "%a, %d %b %Y %H:%M:%S %z")
                if published > last_published:
                    await con.execute ('''INSERT INTO ''' + rss[1] + ''' (title, published, link) VALUES ($1, $2, $3);''', item.title[:255], published, item.link[:255]) 
                    i += 1
                #else:
                    #print(rss[1], published)
            #await conn.execute ('UPDATE rss_url SET etag=$1 WHERE name=$2', rssdates.etag, rss[1]) 
            #print ("Insert news "  +  str(i) ) #+ " in db ===>" + rss[1])
            logger.info("Insert news "  +  str(i) )

    
    except asyncio.TimeoutError as error:
        logger.error(rss[1] + ": WEBSOCKET_TIMEOUT: " + error)
    except (asyncio.CancelledError, KeyboardInterrupt, SystemExit) as error:
        logger.error(rss[1] + ": TASK_CANCELLED: " + error)
    except asyncpg.ConnectionDoesNotExistError:
        pass
    except (asyncpg.CannotConnectNowError, asyncpg.PostgresConnectionError):
        logger.error(rss[1] + ": Postgres CONNECTION ERROR")
    except asyncpg.PostgresError as error: 
        logger.error(rss[1] + ": Postgres other error")
    except OSError:
        logger.error(rss[1] + ": OSError")
    except Exception as error:
        logger.error(rss[1] + ": " + error)
    else:
        logger.info(rss[1] + ": ok!")
    finally:
        await con.close()
        return 0



loop = asyncio.get_event_loop()
loop.run_until_complete(get_rss())
loop.close()


    