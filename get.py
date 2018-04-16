
import feedparser

print "Start read RSS Lenta.ru"
d = feedparser.parse('https://lenta.ru/rss')

print d['feed']['title']
print d['feed']['link']
# print d['feed']['published']
print d['feed']['description']
#d.entries[0]
print len(d.entries)

for item in d.entries:
    print item['title']