import json
import csv
f = open('dataset/yelp_user.csv', 'r',encoding="utf8")
reader = csv.DictReader(f)

jsonoutput = 'dataset/user_new.json'
with open(jsonoutput, 'w') as f:
    for x in reader:
        json.dump(x, f)
        f.write('\n')