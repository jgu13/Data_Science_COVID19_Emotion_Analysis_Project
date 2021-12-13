import src.compute_tf_idfs as tf_idf
import argparse
import json
import os


def main(count_file, num_words):
    with open(count_file, 'r') as f:
        counts = json.load(f)

    tf_idf_values = {}

    for label in counts:
        tf_idf_values[label] = {}
        for sentiment in counts[label]:
            tf_idf_values[label][sentiment] = []
            scores = []
            for word in counts[label][sentiment]:  # catagory-wise tf_idf score calculation
                score = tf_idf.tf_idf(word, counts[label][sentiment], counts[label])
                scores.append((score, word))
            best_scores = sorted(scores, reverse=True)
            for score in best_scores[0:num_words]:
                tf_idf_values[label][sentiment].append(score[1])

    return tf_idf_values


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('count_file')
    parser.add_argument('num_words')
    args = parser.parse_args()
    count_file = args.count_file
    num_words = int(args.num_words)

    output = main(count_file, num_words)
    # print(json.dumps(output, indent=4))

    script_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(script_path, '..', 'data', 'sentiment_tf_idfs.json'), 'w') as f:
        json.dump(output, f, indent=4)
