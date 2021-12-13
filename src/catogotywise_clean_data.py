import os
import argparse
import json
import pandas as pd
import src.clean_data as clean

def add_to_sentiment_count(entry, counts, sentiment):
    if entry in counts[sentiment]:
        counts[sentiment][entry] += 1
    else:
        counts[sentiment][entry] = 1

def remove_rares(total_count, other_dict, min_count):
    for entry in total_count:
        if total_count[entry] < min_count:
            for key in other_dict:
                for sentiment in other_dict[key]:  # remove rare words from every sentiment dictionary
                    other_dict[key][sentiment].pop(entry, None)

def main(tweet_file):
    # make an easily accessible dictionary of stopwords
    script_path = os.path.abspath(os.path.dirname(__file__))
    stop_path = os.path.join(script_path, '..', 'data', 'stopwords.txt')
    stopwords = clean.get_stopwords(stop_path)

    # initialization
    total_count = {}

    # stores the number of times a given word is used by a tweet in each category
    label_count = {
        'covid/pandemic': {'positive': {}, 'negative': {}, 'neutral': {}},
        'economy': {'positive': {}, 'negative': {}, 'neutral': {}},
        'government': {'positive': {}, 'negative': {}, 'neutral': {}},
        'movement': {'positive': {}, 'negative': {}, 'neutral': {}},
        'precaution': {'positive': {}, 'negative': {}, 'neutral': {}},
        'vaccine': {'positive': {}, 'negative': {}, 'neutral': {}},
        'variant': {'positive': {}, 'negative': {}, 'neutral': {}}
    }

    tweets = pd.read_csv(tweet_file, encoding='iso-8859-1')
    for index in range(0, len(tweets)):
        label = tweets.loc[index, 'Label'].casefold()
        if label in label_count:
            words = tweets.loc[index, 'text']
            for word in clean.process_tweet(words, stopwords):
                sentiment = tweets.loc[index, 'Sentiment']
                add_to_sentiment_count(word, label_count[label], sentiment)
                clean.add_to_count(word, total_count)

    # removes words that aren't used at least 5 (can change if necessary) times in total
    remove_rares(total_count, label_count, 5)
    return label_count


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tweet_file', help='Enter the name of the file that contained all the tweets.')
    # parser.add_argument('output_file')
    args = parser.parse_args()

    tweet_file = args.tweet_file

    # if you need to specify different output directories, uncomment this
    #output = os.path.abspath(args.output)
    #output_dir = os.path.dirname(output)
    #if not os.path.isdir(output_dir):
    #    os.makedirs(output_dir)

    label_count = main(tweet_file)

    script_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(script_path, '..', 'data', 'catagorywise_label_words.json'), 'w') as f:
        json.dump(label_count, f, indent=4)
