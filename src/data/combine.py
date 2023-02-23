import pandas as pd
import json
import os
from tqdm import tqdm
import pickle


def get_videoDetails(data, report = False):
    '''return a dataframe of all video details features from Youtube API and a set of failed ids'''

    buffer = []
    failed_ids = set()
    for idx in data.keys():
        if data[idx]['details'] == 'Invalid lookup.':
            failed_ids.add(idx) 
        elif len(data[idx]['details']['items']) == 0:
            failed_ids.add(idx)
        else:
            data[idx]['details']['items'][0]['yt8M_id'] = idx
            buffer.append(data[idx]['details']['items'][0])
    
    videoDets_df = pd.json_normalize(buffer, errors='ignore')
    
    if report:
        print(f'n of videos successful: {videoDets_df.shape[0]}')
        print(f'n of videos failed: {len(failed_ids)}')
    
    return videoDets_df, failed_ids
    

def get_videoComments(data, report=False):
    '''return a dataframe of all comments for videos from Youtube API pull'''
    
    no_comment_count = 0
    buffer = []
    for idx in data.keys():
        if data[idx]['comments'] == 'Invalid lookup':
            no_comment_count += 1
        elif len(data[idx]['comments']['items']) == 0:
            no_comment_count += 1
        else:
            # normalize video comments 
            coms_df = pd.json_normalize(data[idx]['comments']['items'], errors='ignore')
            coms_df['yt8M_id'] = idx
            buffer.append(coms_df)
    
    videoComs_df = pd.concat(buffer,ignore_index=True)

    if report:
        print(f'{no_comment_count = }')

    return videoComs_df


def combine(files_to_combine):
    '''return a videoDetails df, a videoComments df, and a list of failed video_ids for all videos within the API batch results directory'''
    
    failed_ids = set()
    vDets_buffer = []
    vComs_buffer = []
    
    for file in tqdm(files_to_combine):
        with open(file) as file:
            f = json.load(file)
        
        vDets_df, fail_ids = get_videoDetails(f, report=True)
        vDets_buffer.append(vDets_df)
        failed_ids.update(fail_ids)
        
        vComs_df = get_videoComments(f, report=True)
        vComs_buffer.append(vComs_df)
        
    
    vDets = pd.concat(vDets_buffer,ignore_index=True)
    vComs = pd.concat(vComs_buffer,ignore_index=True)
    
    return vDets, vComs, failed_ids


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', help='directory of JSON files (txt)')
    parser.add_argument('output_dir', help='directory to output combined videoDetails pickled dataframe (pkl), videoComments pickled dataframe (pkl), and set of failed ids (pkl)')
    args = parser.parse_args()

    input_files = [os.path.join(args.input_dir, f) 
                    for f in sorted(os.listdir(args.input_dir)) 
                    if f.startswith('batch')]

    videoDets, videoComs, failed_ids = combine(input_files)
    
    with open(os.path.join(args.output_dir, 'videoDets.pkl'), 'wb') as f:
        pickle.dump(videoDets, f)
    
    with open(os.path.join(args.output_dir, 'videoComs.pkl'), 'wb') as f:
        pickle.dump(videoComs, f)

    with open(os.path.join(args.output_dir, 'failed_ids.pkl'), 'wb') as f:
        pickle.dump(failed_ids, f)