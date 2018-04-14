
import feedparser

print "Start read RSS"
d = feedparser.parse('https://www.reddit.com/r/Python/.rss')

print d