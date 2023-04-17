import os
import requests
import re
import json
import pandas as pd
from tqdm import tqdm
import googleapiclient.discovery
import googleapiclient.errors

def api_key(path):
    with open(path) as key_file:
        for line in key_file:
            api_key = line
    return api_key


# collect all of the videos for a topic within a genre
def get_video_ids(genre, topic):
    # get the genre information
    url = 'https://research.google.com/youtube8m/csv/2/vocabulary.csv'
    vocab = pd.read_csv(url)
    topic_df = vocab[(vocab.Vertical1 == genre) | (vocab.Vertical2 == genre) | (vocab.Vertical3 == genre)]
    summary_df = topic_df.groupby(['Name','KnowledgeGraphId']).agg({'TrainVideoCount':'sum'}).reset_index()
    entity2id = dict(zip(summary_df.Name, summary_df.KnowledgeGraphId.str[3:]))
    
    # get the id's for the particular topic
    entity_id = entity2id[topic]
    url = f'https://storage.googleapis.com/data.yt8m.org/2/j/v/{entity_id}.js'
    response = requests.get(url)
    response.raise_for_status() 
    data = response.text
    pattern = r'\w+'
    ids = re.findall(pattern, data)[2:] # video ids start at index 2 onward
    print(f'{topic}({entity_id}): {len(ids)} videos found')

    return ids
    
    
# convert from id to url
def generate_url(vid):
    ''' convert Youtube8M dataset-specific video IDs to true youtube catalog IDs and url '''

    call_str = f'http://data.yt8m.org/2/j/i/{vid[:2]}/{vid}.js'
    res = requests.get(call_str)
    res_lst = res.text.split('"')

    yt_id = res_lst[3]
    url = f'https://www.youtube.com/watch?v={yt_id}'

    return yt_id, url
    
    
# get video data
def video_data_grabber(vid, api_key):
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
      api_service_name, api_version, developerKey=api_key
      )
    request = youtube.videos().list(
    part="contentDetails,  id, liveStreamingDetails, localizations, player,  recordingDetails, snippet, statistics, status, topicDetails",
    id= vid
    )

    response = request.execute()

    return response


# get comments
def comment_grabber(vid, api_key):
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=api_key
    )

    request = youtube.commentThreads().list(
      part="id, snippet",
      videoId = vid,
      textFormat = "plainText",
      maxResults = 100,
      order = "relevance"
    )

    response = request.execute()

    return response


# write results to file
def dict_writer(path, storage_dict, cur_count, failures = False):
    base_path = path
    if failures == False:
        file_name = "batch_" + str(cur_count) + ".txt"
        full_path = os.path.join(base_path, file_name)
        with open (full_path, "w+") as f:
            f.write(json.dumps(storage_dict))
    else:
        file_name = "failed_lookups.txt"
        full_path = os.path.join(base_path, file_name)
        failed_lookups = {"failed": storage_dict}
        with open (full_path, "w+") as f:
            f.write(json.dumps(failed_lookups))
    print("Wrote {}".format(full_path))

    
# takes in a list of videoIds and gets the title and comments for each
# then writes the results to files in the intermediate path
def lookup_videos(videoIds, path, api1, api2):
    storage_dict = {}
    failure_list = []
    count = 1
       
    for idx, vid in enumerate(videoIds):
        try:
            real_id, vid_url = generate_url(vid)
        except:
            failure_list.append((vid,idx))
            real_id = None
            continue
        try:
            video_details = video_data_grabber(real_id, api1)
        except:
            video_details = "Invalid lookup."
        try:
            video_comments = comment_grabber(real_id, api2)
        except:
            video_comments = "Invalid lookup"
        # create sub dictionary
        video_dict = {"real_id":real_id, "url":vid_url, 
                    "details":video_details,"comments":video_comments}
        storage_dict[vid] = video_dict

        # write to file every 400 lookups
        if idx % 400 == 0 and idx != 0:
            dict_writer(path, storage_dict, count)
        # reset storage_dict
            storage_dict = {}
            count += 1

    # write final value to file
    dict_writer(path, storage_dict, count)
    dict_writer(path, failure_list, 0, failures=True)