import argparse
import json
import os
import pandas as pd


# to use:       clean_data.py ../data/complete_filtered_data.csv


def process_tweet(str, stopwords):
    output = []
    str = str.casefold()

    # uses the punctuation from assignment 8: we could modify it if it isn't working well
    punctuation = ['(', ')', '[', ']', ',', '-', '.', '?', '!', ':', ';', '#', '&']
    for char in punctuation:
        str = str.replace(char, ' ')
    words = str.split()
    for word in words:
        # removes common words and mentions ("@username")
        if word in stopwords or word[0] == '@':
            continue
        if word.isalpha():
            output.append(word)
    return output


def get_stopwords(file):
    stopwords = {}
    with open(file, 'r') as f:
        for line in f:
            if line[0] == '#':
                continue
            # I use a dictionary with dummy values since it's a bit faster than searching a list
            stopwords[line.rstrip()] = 0
    return stopwords


def add_to_count(entry, counts):
    if entry in counts:
        counts[entry] += 1
    else:
        counts[entry] = 1


def remove_rares(total_count, other_dict, min_count):
    for entry in total_count:
        if total_count[entry] < min_count:
            for key in other_dict:
                other_dict[key].pop(entry, None)


def main(tweet_file):
    # make an easily accessible dictionary of stopwords
    script_path = os.path.abspath(os.path.dirname(__file__))
    stop_path = os.path.join(script_path, '..', 'data', 'stopwords.txt')
    stopwords = get_stopwords(stop_path)

    # initialization
    total_count = {}

    # stores the number of times a given word is used by a tweet in each category
    label_count = {
        'covid/pandemic': {},
        'economy': {},
        'government': {},
        'movement': {},
        'others': {},
        'precaution': {},
        'vaccine': {},
        'variant': {}
    }

    # stores the number of positive/negative/neutral tweets for each category
    sentiments_count = {
        'covid/pandemic': {'p': 0, 'n': 0, 'r': 0},
        'economy': {'p': 0, 'n': 0, 'r': 0},
        'government': {'p': 0, 'n': 0, 'r': 0},
        'movement': {'p': 0, 'n': 0, 'r': 0},
        'others': {'p': 0, 'n': 0, 'r': 0},
        'precaution': {'p': 0, 'n': 0, 'r': 0},
        'vaccine': {'p': 0, 'n': 0, 'r': 0},
        'variant': {'p': 0, 'n': 0, 'r': 0}
    }

    tweets = pd.read_csv(tweet_file, encoding='iso-8859-1')
    for index in range(0, len(tweets)):
        label = tweets.loc[index, 'Label'].casefold()
        if label in label_count:
            # this could be used to calculate sentiment numbers once annotations are done
            # or
            '''
            if label != 'others':
                sentiment = tweets.loc[index, 'Sentiment'].casefold()
                sentiments_count[label][sentiment] += 1
            '''

            words = tweets.loc[index, 'text']
            for word in process_tweet(words, stopwords):
                add_to_count(word, label_count[label])
                add_to_count(word, total_count)

    # removes words that aren't used at least 5 (can change if necessary) times in total
    remove_rares(total_count, label_count, 5)

    return label_count, sentiments_count


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tweet_file')
    # parser.add_argument('output_file')
    args = parser.parse_args()

    tweet_file = args.tweet_file

    # if you need to specify different output directories, uncomment this
    #output = os.path.abspath(args.output)
    #output_dir = os.path.dirname(output)
    #if not os.path.isdir(output_dir):
    #    os.makedirs(output_dir)

    label_count, sentiments_count = main(tweet_file)

    script_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(script_path, '..', 'data', 'label_words.json'), 'w') as f:
        json.dump(label_count, f, indent=4)
    with open(os.path.join(script_path, '..', 'data', 'label_sentiments.json'), 'w') as f:
        json.dump(sentiments_count, f, indent=4)
