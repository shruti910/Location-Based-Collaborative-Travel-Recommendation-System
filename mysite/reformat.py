import json
import time

start_time = time.time()

tip_path = 'dataset/tip.json'

'''
def create_user(user_path='dataset/user.json'):
    user_data = []

    # need to parse file line by line and use json.load to parse individual strings
    with open(user_path, encoding="utf8") as f:
        i = 0
        for line in f:
            i = i+1
            user_data.append(json.loads(line))
            if i == 1000000:
                with open('dataset/user_reformat.json', 'w') as outfile:
                    json.dump(user_data, outfile, sort_keys=True, indent=4, separators=(',', ': '))
                break
'''
def create_user(user_path='dataset/user_new.json'):
    user_data = []

    # need to parse file line by line and use json.load to parse individual strings
    with open(user_path, encoding="utf8") as f:
        for line in f:
            user_data.append(json.loads(line))

        with open('dataset/user_reformat.json', 'w') as outfile:
            json.dump(user_data, outfile, sort_keys=True, indent=4, separators=(',', ': '))



def create_review(review_path='dataset/review_new.json'):
    review_data = []

    # need to parse file line by line and use json.load to parse individual strings
    with open(review_path, encoding="utf8") as f:
        i = 0
        for line in f:
            i = i+1
            review_data.append(json.loads(line))
            if i == 5000:
                with open('dataset/review_reformat.json', 'w') as outfile:
                    json.dump(review_data, outfile, sort_keys=True, indent=4, separators=(',', ': '))
                break
            #if i == 300000:
            #    i = 1


    # with open('dataset/review_reformat.json', 'w') as outfile:
    # json.dump(review_data, outfile, sort_keys=True, indent=4, separators=(',', ': '))


def create_checkIn(checkIn_path='dataset/checkin.json'):
    checkIn_data = []

    # need to parse file line by line and use json.load to parse individual strings
    with open(checkIn_path, encoding="utf8") as f:
        for line in f:
            checkIn_data.append(json.loads(line))

    with open('checkin.json', 'w') as outfile:
        json.dump(checkIn_data, outfile, sort_keys=True, indent=4, separators=(',', ': '))


def create_business(business_path='dataset/cost_rest.json'):
    business_data = []
    # d=json.loads(business_path.replace('\r\n',''))
    # need to parse file line by line and use json.load to parse individual strings
    with open(business_path, encoding="utf8") as f:
        for line in f:
            business_data.append(json.loads(line, strict=False))

    with open('dataset/business_new.json', 'w') as outfile:
        json.dump(business_data, outfile, sort_keys=True, indent=4, separators=(',', ': '))

    # with open('business.json', 'w') as outfile:
    #    json.dump(d,outfile)


def create_tip(tip_path='dataset/tip.json'):
    tip_data = []

    # need to parse file line by line and use json.load to parse individual strings
    with open(tip_path, encoding="utf8") as f:
        for line in f:
            tip_data.append(json.loads(line))

    with open('tip.json', 'w') as outfile:
        json.dump(tip_data, outfile, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    #create_user()
    #create_review()
    # create_checkIn()
    create_business()
    # create_tip()

    # my machine --- 408 seconds apprx 7 min
    print("--- %s seconds ---" % (time.time() - start_time))