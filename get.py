
import feedparser

print ("Start read RSS Lenta.ru")
d = feedparser.parse('https://lenta.ru/rss')

print (d.version)
print (d.feed.title)
print (d.feed.link)
print (d.feed.description)

print (len(d.entries))

for item in d.entries:
    print ("-----------------------------------", "\n")
    print (item.title, "\n", item.title_detail.value, "\n")
    print ("##########################", "\n")
    print (item.summary, "\n")
    print ("##########################", "\n")
    print (item.summary_detail.value, "\n")
    print ("##########################", "\n")
    print (item.published)
    print ("##########################", "\n")
    print (item.link)



    