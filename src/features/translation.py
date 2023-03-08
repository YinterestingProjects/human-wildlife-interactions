import pickle
import pandas as pd
import fasttext
from transformers import pipeline
from tqdm import tqdm
import re


def clean_text(text):
    # remove spacing
    text = text.replace('\r\n', '')
    text = text.replace('\n', '')

    # remove urls
    text = re.sub(r'http\S+', '', text)
    return text
  

def detect_language(text):
    '''function to detect the language of a single text string'''
    labels, scores = language_detector.predict(text)
    label = labels[0].replace("__label__", '')
    score = round(scores[0], 4)
    return label, score


def translate_text(text, source_language, target_language):
    '''function to translate a single text string from a foreign language to English'''
    if source_language == 'en':
        return text
    else:
        try: 
            results = translator(text, max_length=400, # model max = 1024
                                 src_lang=source_language, tgt_lang=target_language)
            return results[0]['translation_text']
        except KeyError:
            return 'source language unavailable for translation'


def translate_df_column(df, column_to_translate, col_prefix):
    '''function to translate a specified column in a Pandas DataFrame from a foreign language to English''' 
    
    pref = col_prefix
    # cleaning
    df[f'{pref}_clean'] = df[column_to_translate].apply(clean_text)
    
    # language detection
    df[f'{pref}_src_lang'], df[f'{pref}_src_conf'] = zip(*df[f'{pref}_clean'].apply(detect_language))

    # english translation
    tqdm.pandas(desc=f'{pref} translation')
    df[f'{pref}_en'] = df.progress_apply(lambda x: translate_text(text=x[f'{pref}_clean'], 
                                                                  source_language=x[f'{pref}_src_lang'], 
                                                                  target_language='en'
                                                                  ), axis=1)
    
    return df


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input_fp', help='file path of pickled dataframe (pkl)')
    parser.add_argument('src_column', help='name of the dataframe column to be translated (str)')
    parser.add_argument('prefix', help='prefix for translated columns (str)')
    parser.add_argument('output_fp', help='file path pickled dataframe with translations (pkl)')
    args = parser.parse_args()

    # load the pre-trained language detection model and translation pipeline
    language_detector = fasttext.load_model('../../models/lid.176.ftz')
    translator = pipeline('translation', model='facebook/m2m100_418M')

    # translation
    with open(args.input_file, 'rb') as f:
        df = pickle.load(f)
    
    translated_df = translate_df_column(df, args.src_column, args.prefix)
    translated_df.to_pickle(args.output_fp)
