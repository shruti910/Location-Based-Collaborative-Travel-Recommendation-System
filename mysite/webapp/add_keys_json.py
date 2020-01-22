import json
import  random

with open('E:\\projectStart\\mysite\\webapp\\static\\personal\\tourist_final1.json',
          encoding='utf-8') as j_file:
    jfile = json.load(j_file)

digits=2
for dict1 in jfile:
    dict1['stars']=round(random.uniform(3,5),digits)

with open('E:\\projectStart\\mysite\\webapp\\static\\personal\\tourist_final1.json','w') as j_file:
    json.dump(jfile,j_file)