# import urllib.parse
# import json

# input_file = "missing_labels2.txt"
# base_url = "https://vatgia.com/home/"
# sitemap = {"_id": "vatgia", "startUrl": []}

# # Read items from input file
# with open(input_file, "r", encoding='utf-8') as file:
#     items = file.read().splitlines()

# startURL = []
# for item in items:
#     # encoded_item = urllib.parse.quote(item.lower().replace(" ", "%2c"))
#     temp = item.lower().replace(" ", "+")
#     # Encode the modified item for URL
#     encoded_item = urllib.parse.quote(temp)
#     url = base_url + encoded_item + ".spvg"
#     sitemap["startUrl"].append(url)

# output_file = "sitemap2.json"
# # # Save sitemap to JSON file
# # with open(output_file, "w", encoding='utf-8') as file:
# #     for item in startURL:
# #         file.write('"'+ item + '",')
# # Save sitemap to JSON file
# with open(output_file, "w", encoding='utf-8') as file:
#     json.dump(sitemap, file)

# print(f"Sitemap JSON saved to {output_file}")

# '''{"_id":"vatgia","startUrl":[]}'''

# import pandas as pd

# data = pd.read_csv('missing3.csv')
# columns = ['start-url', 'title']
# new = data[columns]
# new.to_csv('missing2.csv', index=False)

import urllib.parse
import pandas as pd

# Read the CSV file
df = pd.read_csv('missing2.csv')

# Function to remove the specified part from the URL
def remove_part(url):
    return url.replace('https://vatgia.com/home/', '')

# Function to decode URL-encoded string to UTF-8 and capitalize the first letter
def decode_and_capitalize(url):
    utf8_string = urllib.parse.unquote(url, encoding='utf-8')
    result = utf8_string.replace('+', ' ')
    result = result.capitalize()
    return result

def remove_tail(url):
    return url.replace('.spvg', '')

# Remove the specified part from the URLs in the first column
df['start-url'] = df['start-url'].apply(remove_part)

# Replace URLs in the first column with the decoded and capitalized strings
df['start-url'] = df['start-url'].apply(decode_and_capitalize)

df['start-url'] = df['start-url'].apply(remove_tail)

df.to_csv('final_missing2.csv', index=False)