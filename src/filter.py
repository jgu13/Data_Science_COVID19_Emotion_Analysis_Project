import json
import os
import pandas as pd
import random
import re


with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "streamed_data2.json"), mode="r") as f:
    df = pd.DataFrame(json.load(f)['data'])

places = ["Canada", "Ottawa",
            "Alberta", "Edmonton",
            "British Columbia", "Victoria",
            "Manitoba", "Winnipeg",
            "New Brunswick", "Fredericton",
            "Newfoundland", "Labrador", "St. John's",
            "Nova Scotia", "Halifax",
            "Ontario", "Toronto",
            "Prince Edward Island", "Charlottetown",
            "Quebec", "Quebec City", "Montreal",
            "Saskatchewan", "Regina",
            "Northwest Territories", "Yellowknife",
            "Nunavut", "Iqaluit",
            "Yukon", "Whitehorse",
          "CA", "AB", "BC", "MB", "NB", 'NL', "NS", 'ON', 'PE', 'QC',
          "SK", "YT", "NU", "NT"
]
def location_filter(locations):
    for p in places:
        pattern = re.compile(p)
        for location in locations:
            if pattern.search(location) is not None:
                return True
    return False
# sample = df[df['user_locations'].apply(location_filter)].sample(frac=0.55)
output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "complete_filtered_data.csv")
# sample.to_csv(path_or_buf=output_path, sep=',', columns=['text'], index=False)
df.to_csv(path_or_buf=output_path, sep=',', columns=['text'], index=False)