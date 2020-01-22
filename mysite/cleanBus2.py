import json


def exists_hotel(arr):
    for element in arr:
        if (element == 'Hotels & Travel') or (element == 'Hotels'):
            return True
    return False

def exists_rest(arr):
	for element in arr:
		if (element=='Fast Food') or (element=='Restaurants')or (element=='Sandwiches') or (element=='Nightlife')or (element=='Bars') or(element=='Burgers') or (element=='Food') or (element=='Breakfast & Brunch') or (element=='Coffee & Tea'):
			return True

	return False

def delete():
    hotel_dict = {}
    with open('dataset/business_new.json') as j_file:
        businessFile = json.load(j_file)
    for business in businessFile:
        if exists_hotel(business['categories']):
            id = business['business_id']
            hotel_dict[id] = {}  # delcare new dict
            hotel_dict[id]['name'] = business['name']  # insert value
            hotel_dict[id]['address'] = business['address']  # insert value
            hotel_dict[id]['city'] = business['city']  # insert value
            hotel_dict[id]['state'] = business['state']  # insert value
            hotel_dict[id]['postal_code'] = business['postal_code']  # insert value
            hotel_dict[id]['latitude'] = business['latitude']  # insert value
            hotel_dict[id]['longitude'] = business['longitude']  # insert value
            hotel_dict[id]['stars'] = business['stars']
            hotel_dict[id]['review_count'] = business['review_count']
            hotel_dict[id]['cost']=business['c']
    with open('dataset/hotel.json', 'w') as outfile:
            json.dump(hotel_dict, outfile, sort_keys=True, indent=4, separators=(',', ': '))


def delete2():
    restaurant_dict = {}
    with open('dataset/business_new.json') as j_file:
        businessFile = json.load(j_file)
    for business in businessFile:
        if exists_rest(business['categories']):
            id = business['business_id']
            restaurant_dict[id] = {}  # delcare new dict
            restaurant_dict[id]['name'] = business['name']  # insert value
            restaurant_dict[id]['address'] = business['address']  # insert value
            restaurant_dict[id]['city'] = business['city']  # insert value
            restaurant_dict[id]['state'] = business['state']  # insert value
            restaurant_dict[id]['postal_code'] = business['postal_code']  # insert value
            restaurant_dict[id]['latitude'] = business['latitude']  # insert value
            restaurant_dict[id]['longitude'] = business['longitude']  # insert value
            restaurant_dict[id]['stars'] = business['stars']
            restaurant_dict[id]['review_count'] = business['review_count']
            restaurant_dict[id]['cost']=business['c']
    with open('dataset/restaurant.json', 'w') as outfile:
            json.dump(restaurant_dict, outfile, sort_keys=True, indent=4, separators=(',', ': '))


if __name__=='__main__':
    delete()
    delete2()