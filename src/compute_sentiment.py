import pandas as pd
import json
import argparse


def compile_sentiment_counts(diag_file_path):
    with open(diag_file_path, mode='rb') as f:
        df = pd.read_csv(f, usecols=['Label', 'Sentiment'],
                         encoding='utf-8', encoding_errors='ignore')  # choose to ignore encoding error

    sentiment_dict = {"vaccine": {'positive': 0, 'negative': 0, 'neutral': 0},
                      "economy": {'positive': 0, 'negative': 0, 'neutral': 0},
                      "variant": {'positive': 0, 'negative': 0, 'neutral': 0},
                      "covid/pandemic": {'positive': 0, 'negative': 0, 'neutral': 0},
                      "movement": {'positive': 0, 'negative': 0, 'neutral': 0},
                      "government": {'positive': 0, 'negative': 0, 'neutral': 0},
                      "precaution": {'positive': 0, 'negative': 0, 'neutral': 0}}

    # count sentiment
    for i, p in enumerate(df['Label']):
        if p.lower() in sentiment_dict.keys():
            if df['Label'][i] != 'others':
                sentiment = df['Sentiment'][i]
                count = sentiment_dict[p.lower()].get(sentiment)
                sentiment_dict[p.lower()][sentiment] = count + 1

    for k, d in sentiment_dict.items():
        count_sum = sum(d.values())
        sentiment_dict[k]['positive'] = round((sentiment_dict[k]['positive'] * 100) / count_sum, 2)
        sentiment_dict[k]['negative'] = round((sentiment_dict[k]['negative'] * 100) / count_sum, 2)
        sentiment_dict[k]['neutral'] = round((sentiment_dict[k]['neutral'] * 100) / count_sum, 2)

    return sentiment_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse input and output file paths.")
    parser.add_argument("-o", "--output_file_path", help="Output file path.")
    parser.add_argument("-d", "--input_file_path", help="Input file path.")
    args = parser.parse_args()
    diag_file_path = args.input_file_path
    output_file_path = args.output_file_path
    sent_dict = compile_sentiment_counts(diag_file_path)
    if output_file_path != None:
        with open(output_file_path, mode='w') as o:
            json.dump(sent_dict, o, indent='\t')
