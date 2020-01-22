import json
import numpy as np
from scipy.sparse import *

import time

start_time = time.time()


# checks if a given business is a restaurant
def is_hotel(a_dict, key):
    if key in a_dict:
        return True
    else:
        return False


def create_h_dict():
    reviewFile = []
    hotelFile = []
    user_ctr = 0
    item_ctr = 0
    all_users = {}
    all_items = {}
    user_indices = []
    item_indices = []
    ratings = []
    print('shruti')
    # load json
    with open('dataset/review_reformat.json') as j_file:
        reviewFile = json.load(j_file)

    with open('dataset/hotel.json') as j_file:
        hotelFile = json.load(j_file)

    for review in reviewFile:
        b_id = review['business_id']

        # consider restaurants only
        if is_hotel(hotelFile, b_id):
            u_id = review['user_id']
            num_stars = review['stars']

            # build the dict of users (so as to map their IDs to values 0,...)
            if u_id not in all_users:

                all_users[u_id] = user_ctr
                u_idx = user_ctr
                #print('u', user_ctr, '', u_idx)
                user_ctr += 1
            else:
                u_idx = all_users[u_id]

            # build the dict of items (so as to map their IDs to values 0,...)
            if b_id not in all_items:

                all_items[b_id] = item_ctr
                b_idx = item_ctr
                #print('i', item_ctr, '', b_idx)
                item_ctr += 1
            else:
                b_idx = all_items[b_id]

            user_indices.append(u_idx)
            item_indices.append(b_idx)
            ratings.append(num_stars)

    print('[%.2f] Building the sparse matrix...' % (time.time() - start_time))
    #print(user_indices)
   # print(item_indices)
    #print(ratings)
    # sort the ratings by users
    tuples = zip(ratings, user_indices, item_indices)
    ratings_sorted, user_indices_sorted, item_indices_sorted = zip(*sorted(tuples, key=lambda x: x[1]))

    # build a sparse matrix from the extracted ratings
    hotel_rating_matrix = coo_matrix((ratings_sorted, (user_indices_sorted, item_indices_sorted)), shape=(user_ctr, item_ctr),
                               dtype=np.uint8)
    print(hotel_rating_matrix.data)
    print(hotel_rating_matrix.row)
    print(hotel_rating_matrix.col)
    print(hotel_rating_matrix.shape)


    print('[%.2f] Saving the mappings...' % (time.time() - start_time))
    np.savez('dataset/hotel_ratingMatrix.npz', data=hotel_rating_matrix.data, row=hotel_rating_matrix.row, col=hotel_rating_matrix.col,shape=hotel_rating_matrix.shape)


    with open('dataset/h_userMapping.json', 'w') as userOut:
        json.dump(all_users, userOut, sort_keys=True, indent=4, separators=(',', ': '))

    with open('dataset/h_itemMapping.json', 'w') as itemOut:
        json.dump(all_items, itemOut, sort_keys=True, indent=4, separators=(',', ': '))

    print("--- %.2f seconds ---" % (time.time() - start_time))
create_h_dict()