import pandas as pd
import os.path as osp
from pathlib import Path
import re
import json
import argparse


def compile_word_counts(diag_file_path):
    stop_words = osp.join(Path(__file__).parents[1], 'data', 'stopwords.txt')
    with open(diag_file_path, mode='rb') as f:
        df = pd.read_csv(f, usecols=['text', 'Label', 'Sentiment'],
                         encoding='utf-8', encoding_errors='ignore')  # choose to ignore encoding error
    with open(stop_words, mode='r') as f:
        stopwords = f.read().splitlines()  # get the list of stopwords

    def remove_stopword(matched_word):
        if matched_word.group(0).lower() in stopwords:
            return ""
        else:
            return matched_word.group(0)

    for i in range(len(df['text'])):
        if pd.isna(df['text'][i]):
            df['text'][i] = ""
        else:
            df['text'][i] = re.sub('@\w+\s', '', df['text'][i])  # remove all mentions
            df['text'][i] = re.sub('#\w+\s', '', df['text'][i])  # remove all hashtags
            df['text'][i] = re.sub('[\(\)\[\],\-.?!:;#&/œ™â¤˜žÃ©%³$ï®ª£½]+', '', df['text'][i])  # replace special characters with a whitespace
            df['text'][i] = re.sub(r'\b[a-zA-Z]+\b', remove_stopword, df['text'][i])  # replace stopwords

    # df.to_csv(osp.join(Path(__file__).parents[1], 'data', 'processed_dialog.csv'), index=False)

    # # count all words that appear at least 5 times across all speech act
    # all_words = {}
    # pattern = re.compile(r"\b[a-zA-Z0-9]+\b")
    # for l in df['dialog']:
    #     words = pattern.findall(l)
    #     for w in words:
    #         count = all_words.get(w.lower(), 0)
    #         all_words[w.lower()] = count + 1
    #
    # invalid = [w for w, c in all_words.items() if c < 5]
    # print(invalid)
    # # df = pd.read_csv(osp.join(Path(__file__).parents[1], 'data', 'processed_dialog.csv'))
    word_dict = {"vaccine": {'sentiments': {'positive': 0, 'negative': 0, 'neutral': 0}, 'words': {}},
                      "economy": {'sentiments': {'positive': 0, 'negative': 0, 'neutral': 0}, 'words': {}},
                      "variant": {'sentiments': {'positive': 0, 'negative': 0, 'neutral': 0}, 'words': {}},
                      "covid/pandemic": {'sentiments': {'positive': 0, 'negative': 0, 'neutral': 0}, 'words': {}},
                      "movement": {'sentiments': {'positive': 0, 'negative': 0, 'neutral': 0}, 'words': {}},
                      "goverment": {'sentiments': {'positive': 0, 'negative': 0, 'neutral': 0}, 'words': {}},
                      "precaution": {'sentiments': {'positive': 0, 'negative': 0, 'neutral': 0}, 'words': {}},
                      "others": {'sentiments': {'positive': 0, 'negative': 0, 'neutral': 0}, 'words': {}}}

    # count words for every pony
    pattern = re.compile(r'\b[a-zA-Z0-9]+\b')
    for i, p in enumerate(df['text']):
        if p.lower() in word_dict.keys():
            # print(p.lower())
            words = pattern.findall(df['text'][i])
            # print(words)
            for w in words:
                count = word_dict[p.lower()]['words'].get(w.lower(), 0)
                word_dict[p.lower()]['words'][w.lower()] = count+1
            if df['Label'][i] != 'others':
                sentiment = df['Sentiment'][i]
                count = word_dict[p.lower()]['sentiments'].get(sentiment)
                word_dict[p.lower()]['sentiments'][sentiment] = count + 1

    return pony_word_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse input and output file paths.")
    parser.add_argument("-o", "--output_file_path", help="Output file name must be word_counts.json")
    parser.add_argument("-d", "--input_file_path", help="Input file must be clean_dialog.csv")
    args = parser.parse_args()
    diag_file_path = args.input_file_path
    output_file_path = args.output_file_path
    pony_word_dict = compile_word_counts(diag_file_path)
    if output_file_path != None:
        with open(output_file_path, mode='w') as o:
            json.dump(pony_word_dict, o, indent='\t')
