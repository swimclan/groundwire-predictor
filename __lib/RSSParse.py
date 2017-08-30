import xml.etree.ElementTree as ET
import utils

def parse(doc):
    ret = {}
    rss = ET.fromstring(doc)
    channel = rss.find('channel')
    ret['copyright'] = channel.find('copyright').text
    ret['description'] = channel.find('description').text
    items = channel.findall('item')
    news_items = []
    for item in items:
        news_items.append({
            'description': item.find('description').text,
            'guid': item.find('guid').text,
            'link': item.find('link').text,
            'pubDate': utils.parsePubDate(item.find('pubDate').text),
            'title': item.find('title').text
        })
    ret['items'] = news_items
    ret['language'] = channel.find('language').text
    ret['lastBuildDate'] = channel.find('lastBuildDate').text
    ret['link'] = channel.find('link').text
    ret['title'] = channel.find('title').text
    return ret
