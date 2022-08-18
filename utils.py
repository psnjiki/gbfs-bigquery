from datetime import datetime, timezone

import requests
from dateutil import tz


DATA_KEY = "data"
FEEDS_KEY = "feeds"
URL_KEY = "url"
NAME_KEY = "name"
TZ_KEY = "timezone"
SYS_INFO_KEY = "system_information"


def get_feeds(url, lang="en"):
    query_time = datetime.now(timezone.utc)
    gbfs = requests.get(url).json() #gbfs home
    
    feeds_url_list = gbfs[DATA_KEY][lang][FEEDS_KEY] # feeds listed
    
    # collect raw feeds
    feeds = {}
    for feed_dict in feeds_url_list:
        feeds[feed_dict[NAME_KEY]] = requests.get(feed_dict[URL_KEY]).json()
    
    # convert query time to system time zone
    time_zone_name = feeds[SYS_INFO_KEY][DATA_KEY][TZ_KEY]
    query_time = query_time.astimezone(tz.gettz(time_zone_name))
    query_time = int(datetime.timestamp(query_time))
    #query_time = query_time.strftime("%Y-%m-%d %H:%M:%S")
    
    # update raw feeds: grab data key, plus report time
    for name, feed in feeds.items():
        feed["query_time"] = query_time
        if len(feed[DATA_KEY]) == 1: # dig deeper if single key
            key = list(feed[DATA_KEY].keys())[0]
            feed_data = feed.pop(DATA_KEY)
            for i in range(len(feed_data[key])):
                feed_data[key][i]= {
                    **feed,
                    **feed_data[key][i]
                    }
            feeds[name] = feed_data[key]
        else:
            feed_data = feed.pop(DATA_KEY)
            feed_data = {
                **feed,
                **feed_data
                }
            feeds[name] = feed_data
    return feeds
 