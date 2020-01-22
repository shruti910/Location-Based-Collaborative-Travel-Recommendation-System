import json


def delete():
    user_dict = {}
    with open('dataset/user.json') as j_file:
        userFile = json.load(j_file)
    for user in userFile:
        id = user['user_id']
        user_dict[id] = {}  # delcare new dict
        user_dict[id]['business_id'] = user['business_id']  # insert value
        #user_dict[id]['review_count'] = user['review_count']  # insert value
        #user_dict[id]['average_stars'] = user['average_stars']  # insert value
        #user_dict[id]['friends'] = business['friends']  # insert value
    with open('dataset/user_new.json', 'w') as outfile:
        json.dump(user_dict, outfile, sort_keys=True, indent=4, separators=(',', ': '))


if __name__=='__main__':
    delete()