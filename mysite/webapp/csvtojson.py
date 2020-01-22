import csv
import json
data=[]
with open('E:\\projectStart\\mysite\\webapp\\static\\datasets\\final_rest.csv') as f:
    for row in csv.DictReader(f):
        data.append(row)


with open('E:\\projectStart\\mysite\\webapp\\static\\datasets\\final_rest.json','w') as outfile:
    json.dump(data,outfile)