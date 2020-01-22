import json
user='cQpQvH9VNwtWkDXQEzM-cg'
with open('E:\\projectStart\\mysite\\webapp\\static\\personal\\place_user_rating.json', encoding='utf-8') as f:
    pFile = json.load(f)
pFile = [x for x in pFile if x['user_id'] == user]
print(pFile)