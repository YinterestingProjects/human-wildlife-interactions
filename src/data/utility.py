import pandas as pd
import requests


# get all video ids
vocab_file = 'https://research.google.com/youtube8m/csv/2/vocabulary.csv'
vocab_df = pd.read_csv(vocab_file)

animal_df = vocab_df[(vocab_df.Vertical1 == 'Pets & Animals') | (vocab_df.Vertical2 == 'Pets & Animals')] # Pets & Animal only present in V1&2
summary_df = animal_df.groupby(['Name','KnowledgeGraphId']).agg({'TrainVideoCount':'sum'}).reset_index()

# create entity to id lookup dictionary 
entity2id = dict(zip(summary_df.Name, summary_df.KnowledgeGraphId.str[3:]))

def get_entity_videoIDs(entity_name):
''' gets a list of video ids in the YT8M training dataset tagged with a given entity(name)'''

    entity_id = entity2id[entity_name]

    api_url = f'https://storage.googleapis.com/data.yt8m.org/2/j/v/{entity_id}.js'
    response = requests.get(api_url)
    response.raise_for_status() 

    data = response.text
    pattern = r'\w+'
    ids = re.findall(pattern, data)[2:] # video ids start at index 2 onward
    print(f'{entity_name}({entity_id}): {len(ids)} videos found')

    return ids


def get_yt_url(id):
''' convert Youtube8M dataset-specific video IDs to true youtube catalog IDs and url '''
 
    api_url = f'http://data.yt8m.org/2/j/i/{id[:2]}/{id}.js'
    response = requests.get(api_url)
    
    res_lst = res.text.split('"')
    yt_id = res_lst[3]
    url = f'https://www.youtube.com/watch?v={yt_id}'

    return yt_id, url

