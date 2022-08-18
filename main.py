import os
import json
from google.cloud import bigquery
from utils import get_feeds, SYS_INFO_KEY


LAST_UPDATE_KEY = "last_updated"

if __name__ == "__main__":
    # default: use params.json to set default opserator
    # alternatively, submit environments variables with the run command
    if os.getenv("URL") is None: 
        with open("params.json", "r") as file:
            params = json.load(file)
    else:
        params = {
            "FEEDS_LANGUAGE": os.getenv("FEEDS_LANGUAGE"),
            "DATASET_ID": os.getenv("DATASET_ID"),
            "URL": os.getenv("URL")
            }

    # get gbfs feeds
    feeds = get_feeds(
        url=params["URL"],
        lang=params["FEEDS_LANGUAGE"]
        )  
    
    # set up bigquery client
    bq = bigquery.Client()
    dataset_id = params["DATASET_ID"]
    
    # save each feed in its own bigquery table,
    # except for SYS_INFO_KEY feed mostly redondant
    for feed_name in set(feeds.keys()) - {SYS_INFO_KEY}:
        
        table_id = f"{dataset_id}.{feed_name}"
        
        data = feeds[feed_name]
        if not type(data) is list:
            data = [data]      
    
        # check if data is empty
        if len(data) == 0:
            print(f"skip empty feed {feed_name}.")
            continue
        
        # load feed to bq
        job = bq.load_table_from_json(data, destination=table_id)
        job.result() # wait for job to complete