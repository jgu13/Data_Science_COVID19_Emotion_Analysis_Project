import json
import os
import pandas as pd
import random
import re


with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "streamed_data3.json"), mode="r") as f:
    df = pd.DataFrame(json.load(f)['data'])

places = ["Canada", "Ottawa",
            "Alberta", "Edmonton", "Calgary",
            "British Columbia", "Victoria", "Vancouver",
            "Manitoba", "Winnipeg",
            "New Brunswick", "Fredericton",
            "Newfoundland", "Labrador", "St. John's",
            "Nova Scotia", "Halifax",
            "Ontario", "Toronto", "Hamilton", "Windsor", "Mississauga", "Kingston", "Kitchener", "Sudbury", "Waterloo", "waterloo",
            "Prince Edward Island", "Charlottetown",
            "Québec", "Québec City", "Montréal",
            "Saskatchewan", "Regina", "Saskatoon"
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
filtered = df[df['user_locations'].apply(location_filter)]
output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "complete_filtered_data2.csv")
# sample.to_csv(path_or_buf=output_path, sep=',', columns=['text'], index=False)
filtered.to_csv(path_or_buf=output_path, sep=',', columns=['text'], index=False)