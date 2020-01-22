import json
#import config_paths

#simply searches for any hotels in the array of categories
def exists_rest(arr):
	for element in arr:
		if (element=='Fast Food') or (element=='Restaurants')or (element=='Sandwiches') or (element=='Nightlife')or (element=='Bars') or(element=='Burgers') or (element=='Food') or (element=='Breakfast & Brunch') or (element=='Coffee & Tea'):
			return True

	return False

def delete():

	rest_dict={}

	#open json file
	with open('datasets/business.json') as j_file:
		businessFile= json.load(j_file)

	for business in businessFile:
		if exists_rest( business['categories']):
			id = business['business_id'] #take bussines id
			rest_dict[id]={} #delcare new dict
			rest_dict[id]['name']=business['name']
            #rest_dict[id]['categories']=business['categories']
			rest_dict[id]['address']=business['address']
			rest_dict[id]['city']=business['city']
			rest_dict[id]['state']=business['state']
			rest_dict[id]['postal_code'] = business['postal_code']
			rest_dict[id]['latitude'] = business['latitude']
			rest_dict[id]['longitude'] = business['longitude']
			rest_dict[id]['stars'] = business['stars']
			rest_dict[id]['review_count'] = business['review_count']


	with open('datasets/restaurants.json', 'w') as outfile:
		json.dump(rest_dict, outfile, sort_keys=True, indent=4, separators=(',', ': '))



if __name__=='__main__':
	delete()