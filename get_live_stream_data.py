import requests
import os
import json

# To set your environment variables in your terminal run the following line:

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIKXWAEAAAAAkPGelAhulFDupVA3fDxWxTo%2FDkw%3DovdZ2Tx7gy79irhn5uwcHlY5dVtfBZlAmUa0prJnDXnj5rxpO3"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'expansions': 'geo.place_id,author_id', 'place.fields': 'country_code', 'user.fields': 'location',
                'tweet.fields': 'text'}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = "data_collection_bot"
    return r

def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()

def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "(-is:retweet) (covid OR covid-19 OR vaccination OR vaccine OR Pfizer OR Moderna OR (Johnson%26Johnson vaccine)) -Trump -news -Global -CBC -has:links lang:en (Canada OR Canadian)"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(set):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True, params=query_params
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    with open(os.path.join(os.path.dirname(__file__), "data", "streamed_data2.json"), 'a+') as f:
        f.write('[')
        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                text = json_response['data']['text']
                user_locations = []
                for u in json_response['includes']['users']:
                    user_locations.append(u.get('location', ''))
                country_code = []
                if 'places' in json_response['includes'].keys():
                    for p in json_response['includes']['places']:
                        country_code.append(p['country_code'])
                result = {'text': text, 'user_locations': user_locations, 'country': country_code}
                f.write(json.dumps(result, indent=4, sort_keys=True)+',\n')
                print(result)
        f.write(']')


def main():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    get_stream(set)


if __name__ == "__main__":
    main()