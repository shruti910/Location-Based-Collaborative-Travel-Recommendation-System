import json

user='cQpQvH9VNwtWkDXQEzM-cg'

with open('E:\\projectStart\\mysite\\dataset\\review_reformat.json') as j_file:
    reviewFile = json.load(j_file)

user_review_dict = [x for x in reviewFile if x['user_id'] == user]
print(user_review_dict)
with open('E:\\projectStart\\mysite\\dataset\\user_review_dict.json', 'w') as outfile:
    json.dump(user_review_dict, outfile, sort_keys=True, indent=4, separators=(',', ': '))
with open('E:\\projectStart\\mysite\\dataset\\business_new.json') as j_file:
    busFile = json.load(j_file)
user_review_bus_dict=[]
for u in user_review_dict:
    for x in busFile:
        if (x['business_id'] ==u['business_id']):
            user_review_bus_dict.append(x.copy())

print(user_review_bus_dict)
'''
with open('E:\\projectStart\\mysite\\dataset\\user_review_bus_dict.json', 'w') as outfile:
        json.dump(user_review_bus_dict, outfile, sort_keys=True, indent=4, separators=(',', ': '))
'''
print('heyyyyyyyyyy')

def exists_hotel_rest(arr):
	for element in arr:
		if (element=='Fast Food') or (element=='Restaurants')or (element=='Sandwiches') or (element=='Nightlife')or (element=='Bars') or(element=='Burgers') or (element=='Food') or (element=='Breakfast & Brunch') or (element=='Coffee & Tea')or (element == 'Hotels & Travel') or (element == 'Hotels'):
			return True

	return False
user_review_hot_res = [x for x in user_review_bus_dict if exists_hotel_rest(x['categories'])]
print(user_review_hot_res)
with open('E:\\projectStart\\mysite\\dataset\\user_review_bus_catg.json', 'w') as outfile:
    json.dump(user_review_bus_dict, outfile, sort_keys=True, indent=4, separators=(',', ': '))