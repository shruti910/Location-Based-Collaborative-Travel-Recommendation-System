from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from .forms import SignUpForm,MyModelForm
from django.views.generic import View, CreateView
from django.contrib.auth import authenticate, get_user_model,login
import pandas as pd
import json
import numpy as np
from .forms import ContactForm
from .forms import ValuesForm
from .forms import RateSubmitForm
from .forms import ImgForm
from django.contrib.auth.decorators import login_required
from .models import MyModel
import requests
import recommender_final_r
import recommender_copy_h
import operator

dictionary_r=''
dictionary_h=''
def index(request):
    return render(request,'cover/index.html')


class homepage(CreateView):
    model=MyModel
    form_class=MyModelForm
    template_name = 'home/home.html'

    def get(self,request):
        with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\tourist_final1.json',
                  encoding='utf-8') as j_file:
            jfile=json.load(j_file)

        def extract_stars(json):
            try:
                return float(json['stars'])
            except KeyError:
                return 0
        jfile.sort(key=extract_stars,reverse=True)
        output_dict=[x for x in jfile if float(x['stars'])>4.5]
        form = self.form_class(None)
        form1 = ContactForm()
        hotels = pd.read_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\final_hotels1.csv')
        ratings = pd.read_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\hotel_review.csv')
        ratings.drop(['review_id'], axis=1, inplace=True)
        hotels.drop(['review_count', 'stars'], axis=1, inplace=True)
        dataset = pd.merge(hotels, ratings, how='inner', on='business_id')
        dataset.drop(['Unnamed: 0_x', 'Unnamed: 0_y'], axis=1, inplace=True)

        # print(dataset.head())

        ratings_total = dataset.groupby(['business_id']).size()
        # print(ratings_total.head())

        ratings_mean = (dataset.groupby(['business_id', 'name']))['business_id', 'stars', 'name'].mean()
        # print(ratings_mean.head())
        ratings_mean.to_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\rating_mean.csv')
        # modify the dataframes so that we can merge the two

        ratings_total = pd.DataFrame({'business_id': ratings_total.index, 'total_ratings': ratings_total.values})
        ratings_total.to_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\ratings_total.csv')
        ratings_total = pd.read_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\ratings_total.csv')
        ratings_mean = pd.read_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\rating_mean.csv')
        # ratings_mean['business_id'] = ratings_mean.index
        # ratings_mean['name'] = ratings_mean.index['name']
        # print(ratings_total.head())
        # print(ratings_mean.columns)
        # print(ratings_mean.head())

        # final merge

        final = pd.merge(pd.merge(ratings_mean, ratings_total, how='inner', on='business_id'), hotels, how='inner',
                         on='business_id').sort_values(by='total_ratings',
                                                       ascending=False)

        final.drop(['Unnamed: 0_x', 'Unnamed: 0_y', 'name_y'], axis=1, inplace=True)
        C = final['stars'].mean()  # mean value of rating across whole dataset
        # print(C)
        # print(final.describe())
        # taken 75th %ile
        # Calculate the minimum number of votes required to be in the chart, m
        m = final['total_ratings'].quantile(0.75)
        # print(m)
        # Filter out all qualified restaurants into a new DataFrame
        q_res = final.copy().loc[final['total_ratings'] >= m]

        # Function that computes the weighted rating of each restaurant
        def weighted_rating(x, m=m, C=C):
            v = x['total_ratings']
            R = x['stars']
            # Calculation based on the IMDB formula
            return (v / (v + m) * R) + (m / (m + v) * C)

        # Define a new feature 'score' and calculate its value with `weighted_rating()`
        q_res['score'] = q_res.apply(weighted_rating, axis=1)

        # Sort restaurants based on score calculated above
        q_res = q_res.sort_values('score', ascending=False)
        q_res = q_res.head(15)
        qfinal_res = q_res.to_dict('records')
        '''
        with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\pop_hotel.json',
                  mode='w',encoding='utf-8') as f:
            json.dump(qfinal_res, f, sort_keys=True, indent=4, separators=(',', ': '))

        '''
        restr = pd.read_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\final_rest.csv')
        ratings = pd.read_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\rest_review.csv')
        ratings.drop(['review_id'], axis=1, inplace=True)
        restr.drop(['review_count', 'stars'], axis=1, inplace=True)
        dataset = pd.merge(restr, ratings, how='inner', on='business_id')
        dataset.drop(['Unnamed: 0_x', 'Unnamed: 0_y'], axis=1, inplace=True)

        # print(dataset.head())

        ratings_total = dataset.groupby(['business_id']).size()
        # print(ratings_total.head())

        ratings_mean = (dataset.groupby(['business_id', 'name']))['business_id', 'stars', 'name'].mean()
        ratings_mean.to_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\rating_mean1.csv')
        # modify the dataframes so that we can merge the two
        # print(ratings_mean.head())

        ratings_total = pd.DataFrame({'business_id': ratings_total.index, 'total_ratings': ratings_total.values})
        ratings_total.to_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\ratings_total1.csv')
        ratings_total = pd.read_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\ratings_total1.csv')
        ratings_mean = pd.read_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\rating_mean1.csv')
        # final merge

        final = pd.merge(pd.merge(ratings_mean, ratings_total, how='inner', on='business_id'), restr, how='inner',
                         on='business_id').sort_values(by='total_ratings',
                                                       ascending=False)
        final.drop(['Unnamed: 0_x', 'Unnamed: 0_y', 'name_y'], axis=1, inplace=True)
        C = final['stars'].mean()  # mean value of rating across whole dataset
        # print(C)
        # taken 75th %ile
        # Calculate the minimum number of votes required to be in the chart, m
        m = final['total_ratings'].quantile(0.75)
        # print(m)
        # Filter out all qualified restaurants into a new DataFrame
        q_res1 = final.copy().loc[final['total_ratings'] >= m]

        # Function that computes the weighted rating of each restaurant
        def weighted_rating(x, m=m, C=C):
            v = x['total_ratings']
            R = x['stars']
            # Calculation based on the IMDB formula
            return (v / (v + m) * R) + (m / (m + v) * C)

        # Define a new feature 'score' and calculate its value with `weighted_rating()`
        q_res1['score'] = q_res1.apply(weighted_rating, axis=1)

        # Sort restaurants based on score calculated above
        q_res1 = q_res1.sort_values('score', ascending=False)
        q_res1 = q_res1.head(15)
        qfinal_res1 = q_res1.to_dict('records')
        '''
        with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\pop_rest.json',
                  mode='w',encoding='utf-8') as f:
            json.dump(qfinal_res1, f, sort_keys=True, indent=4, separators=(',', ': '))
        '''
        with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\pop_rest.json', encoding='utf-8') as f:
            pr=json.load(f)
        with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\pop_hotel.json', encoding='utf-8') as f:
            ph=json.load(f)
        return render(request, self.template_name, {'form': form, 'places':output_dict,'photel':ph,'prest':pr})

        #  process form data

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            state=form.cleaned_data['state']

            with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\tourist_final1.json',
                      encoding='utf-8') as j_file:
             tFile = json.load(j_file)

            output_dict = [x for x in tFile if x['state'] == state]
            rec_rest,rec_rest_cost = recommendation_r(request)
            rec_hotel,rec_hotel_cost = recommendation_h(request)
            return render(request, 'personal/display.html', {'contents': output_dict, 'place_name': state,'rec_rest': rec_rest,'rec_hotel': rec_hotel})



def hotels(request):
    hotels = pd.read_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\final_hotels1.csv')
    ratings = pd.read_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\hotel_review.csv')
    ratings.drop(['review_id'], axis=1, inplace=True)
    hotels.drop(['review_count', 'stars'], axis=1, inplace=True)
    dataset = pd.merge(hotels, ratings, how='inner', on='business_id')
    dataset.drop(['Unnamed: 0_x', 'Unnamed: 0_y'], axis=1, inplace=True)

    #print(dataset.head())

    ratings_total = dataset.groupby(['business_id']).size()
    # print(ratings_total.head())

    ratings_mean = (dataset.groupby(['business_id', 'name']))['business_id', 'stars', 'name'].mean()
    #print(ratings_mean.head())
    ratings_mean.to_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\rating_mean.csv')
    # modify the dataframes so that we can merge the two

    ratings_total = pd.DataFrame({'business_id': ratings_total.index, 'total_ratings': ratings_total.values})
    ratings_total.to_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\ratings_total.csv')
    ratings_total = pd.read_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\ratings_total.csv')
    ratings_mean = pd.read_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\rating_mean.csv')
    # ratings_mean['business_id'] = ratings_mean.index
    # ratings_mean['name'] = ratings_mean.index['name']
    # print(ratings_total.head())
    # print(ratings_mean.columns)
    # print(ratings_mean.head())

    # final merge

    final = pd.merge(pd.merge(ratings_mean, ratings_total, how='inner', on='business_id'),hotels,how='inner', on='business_id').sort_values(by='total_ratings',
                                                                                             ascending=False)

    final.drop(['Unnamed: 0_x', 'Unnamed: 0_y','name_y'], axis=1, inplace=True)
    C = final['stars'].mean()  # mean value of rating across whole dataset
    # print(C)
    # print(final.describe())
    # taken 75th %ile
    # Calculate the minimum number of votes required to be in the chart, m
    m = final['total_ratings'].quantile(0.75)
    # print(m)
    # Filter out all qualified restaurants into a new DataFrame
    q_res = final.copy().loc[final['total_ratings'] >= m]

    # Function that computes the weighted rating of each restaurant
    def weighted_rating(x, m=m, C=C):
        v = x['total_ratings']
        R = x['stars']
        # Calculation based on the IMDB formula
        return (v / (v + m) * R) + (m / (m + v) * C)

    # Define a new feature 'score' and calculate its value with `weighted_rating()`
    q_res['score'] = q_res.apply(weighted_rating, axis=1)

    # Sort restaurants based on score calculated above
    q_res = q_res.sort_values('score', ascending=False)
    q_res = q_res.head(15)
    qfinal_res = q_res.to_dict('records')
    with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\pop_hotel.json', encoding='utf-8') as f:
        ph = json.load(f)
    return render(request, 'popular/popular_hotels.html', {'qhotel': ph})



class Signup(View):
    form_class = SignUpForm
    template_name = 'login\signup.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})


    #  process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
             user = form.save(commit=False)

            #cleaned(normalized) data
             username=form.cleaned_data['username']
             password = form.cleaned_data['password1']
             user.set_password(password) # if u want to change the user's password
             user.save()

             #returns User objects if credentials are correct
             user = authenticate(username=username, password=password)

             if user is not None:
                  if user.is_active:
                      login(request,user)
                      return redirect('dashboard')

        return render(request, self.template_name, {'form':form})

def dashboard(request):

    user=request.user.username
    with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\place_user_rating.json', encoding='utf-8') as f:
        pFile = json.load(f)
    pfile=[x for x in pFile if x['user_id'] == user]
    with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\rest_user_rating.json', encoding='utf-8') as f:
        rFile = json.load(f)
    rfile = [x for x in rFile if x['user_id'] == user]
    with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\hotel_user_rating.json', encoding='utf-8') as f:
        hFile = json.load(f)
    hfile = [x for x in hFile if x['user_id'] == user]
    with open('N:\\projectStart\\mysite\\dataset\\review_reformat.json') as j_file:
        reviewFile = json.load(j_file)

    user_review_dict = [x for x in reviewFile if x['user_id'] == user]
    with open('N:\\projectStart\\mysite\\dataset\\business_new.json') as j_file:
        busFile = json.load(j_file)
    user_review_bus_dict = []
    for u in user_review_dict:
        for x in busFile:
            if (x['business_id'] == u['business_id']):
                user_review_bus_dict.append(x.copy())

    '''
    with open('N:\\projectStart\\mysite\\dataset\\user_review_bus_dict.json', 'w') as outfile:
            json.dump(user_review_bus_dict, outfile, sort_keys=True, indent=4, separators=(',', ': '))
    '''

    def exists_hotel_rest(arr):
        for element in arr:
            if (element == 'Fast Food') or (element == 'Restaurants') or (element == 'Sandwiches') or (
                    element == 'Nightlife') or (element == 'Bars') or (element == 'Burgers') or (element == 'Food') or (
                    element == 'Breakfast & Brunch') or (element == 'Coffee & Tea') or (
                    element == 'Hotels & Travel') or (element == 'Hotels'):
                return True

        return False

    user_review_hot_res = [x for x in user_review_bus_dict if exists_hotel_rest(x['categories'])]

    return render(request, 'dashboard/dashboard.html',{'user_review':user_review_hot_res,'pfile':pfile,'rfile':rfile,'hfile':hfile})

def display(request):
    form=ContactForm()
    return render(request,'personal/display.html')

def mapdisplay(request):

    sname=''

    latitude=''
    longitude=''

    if request.method == 'POST' and 'b1' in request.POST:
        form = ContactForm(request.POST)

        if form.is_valid():
            sname=form.cleaned_data['name']

        address = sname
        print(address)
        api_key = "AIzaSyDWtysGuiNFrZVS3MnoqXMT0ToUyLGG1dI"
        api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
        api_response_dict = api_response.json()
        if api_response_dict['status'] == 'OK':
            latitude = api_response_dict['results'][0]['geometry']['location']['lat']
            longitude = api_response_dict['results'][0]['geometry']['location']['lng']
            print(latitude)
            print(longitude)
        return render(request,'personal/mapDisplay.html',{'lat':latitude,'longt':longitude,'address':address})
    if request.method=='POST' and 'b2' in request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            sname = form.cleaned_data['name']
            print(sname)
        return render(request, 'personal/distance_calc.html',{'dest':sname})
    if request.method == 'POST' and 'b3' in request.POST:
        form = ContactForm(request.POST)

        if form.is_valid():
            sname = form.cleaned_data['name']
            print(sname)
        return render(request,'personal/directions.html',{'address':sname})
    if request.method=='POST' and 'b4' in request.POST:
        form = ValuesForm(request.POST)
        if form.is_valid():
            latitude = form.cleaned_data['name1']
            longitude = form.cleaned_data['name2']
            adrs = form.cleaned_data['name3']
            print(latitude)
            print(longitude)
        else:
            return render(request,'cover/index.html')

        return render(request, 'personal/mapDisplay.html',{'lat':latitude,'longt':longitude,'address':adrs})
    if request.method=='POST' and 'b5' in request.POST:
        form = ValuesForm(request.POST)
        sname=''
        if form.is_valid():
            sname = form.cleaned_data['name3']
            print(sname)
        return render(request, 'personal/distance_calc.html',{'dest':sname})
    if request.method == 'POST' and 'b6' in request.POST:
        form = ValuesForm(request.POST)
        sname=''
        if form.is_valid():
            sname = form.cleaned_data['name3']
            print(sname)
        return render(request,'personal/directions.html',{'address':sname})

def restaurants(request):
    restr = pd.read_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\final_rest.csv')
    ratings = pd.read_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\rest_review.csv')
    ratings.drop(['review_id'], axis=1, inplace=True)
    restr.drop(['review_count', 'stars'], axis=1, inplace=True)
    dataset = pd.merge(restr, ratings, how='inner', on='business_id')
    dataset.drop(['Unnamed: 0_x', 'Unnamed: 0_y'], axis=1, inplace=True)

    # print(dataset.head())

    ratings_total = dataset.groupby(['business_id']).size()
    # print(ratings_total.head())

    ratings_mean = (dataset.groupby(['business_id', 'name']))['business_id', 'stars', 'name'].mean()
    ratings_mean.to_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\rating_mean1.csv')
    # modify the dataframes so that we can merge the two
    # print(ratings_mean.head())

    ratings_total = pd.DataFrame({'business_id': ratings_total.index, 'total_ratings': ratings_total.values})
    ratings_total.to_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\ratings_total1.csv')
    ratings_total = pd.read_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\ratings_total1.csv')
    ratings_mean = pd.read_csv('N:\\projectStart\\mysite\\webapp\\static\\datasets\\rating_mean1.csv')
    # final merge

    final = pd.merge(pd.merge(ratings_mean, ratings_total, how='inner', on='business_id'),restr,how='inner', on='business_id').sort_values(by='total_ratings',
                                                                                             ascending=False)
    final.drop(['Unnamed: 0_x', 'Unnamed: 0_y','name_y'], axis=1, inplace=True)
    C = final['stars'].mean()  # mean value of rating across whole dataset
    # print(C)
    # taken 75th %ile
    # Calculate the minimum number of votes required to be in the chart, m
    m = final['total_ratings'].quantile(0.75)
    # print(m)
    # Filter out all qualified restaurants into a new DataFrame
    q_res1 = final.copy().loc[final['total_ratings'] >= m]

    # Function that computes the weighted rating of each restaurant
    def weighted_rating(x, m=m, C=C):
        v = x['total_ratings']
        R = x['stars']
        # Calculation based on the IMDB formula
        return (v / (v + m) * R) + (m / (m + v) * C)

    # Define a new feature 'score' and calculate its value with `weighted_rating()`
    q_res1['score'] = q_res1.apply(weighted_rating, axis=1)

    # Sort restaurants based on score calculated above
    q_res1 = q_res1.sort_values('score', ascending=False)
    q_res1 = q_res1.head(15)
    qfinal_res1 = q_res1.to_dict('records')
    with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\pop_rest.json', encoding='utf-8') as f:
        pr= json.load(f)
    return render(request, 'popular/popular_rest.html', {'qrest': pr})

def recommendation_r(request):
    #name = request.user.username
    #print(name)
    id=request.user.username
   # name=request.user.first_name
    #print(name)
    rec_system = recommender_final_r.RecommenderFinal()

    # training
    print('\nTraining data:')
    print('-> Number of ratings:  %s' % len(rec_system.ratings_train.data))
    print('-> Number of distinct users:  %s' % len(np.unique(rec_system.ratings_train.row)))
    print('-> Number of distinct items:  %s' % len(np.unique(rec_system.ratings_train.col)))
    print('-> Number of latent factors:  %d' % (rec_system.num_user_factors))


    '''
    rec_system.train()
    
    print('\nLearned values:')
    print('\n-> User factors:')
    print(rec_system.user_factors)
    print('\n-> Item factors:')
    print(rec_system.item_factors)
    
    # testing
    print('\nTest data:')
    print('-> Number of ratings:  %s' % len(rec_system.ratings_test.data))
    print('-> Number of distinct users:  %s' % len(np.unique(rec_system.ratings_test.row)))
    print('-> Number of distinct items:  %s' % len(np.unique(rec_system.ratings_test.col)))

    test_rmse = rec_system.test()
    # test_rmse = rec_system.test_baseline()
    # test_rmse = rec_system.test_naive()

    print('\nRMSE: %s\n' % test_rmse)
    '''

    # rec_system.test_example()
    # recommendation of top items for a specific user
    user_id = id
    num_items = 20
    rec_system.recommend(user_id, num_items)
    rec_pre=rec_system.top_predictions
    rec_rest=rec_system.top_rest_names
    rec_rest_cost = rec_system.top_rest_cost
    dictionary_r = dict(zip(rec_rest, rec_pre))
    dictionary_r_cost = dict(zip(rec_rest, rec_rest_cost))
    print(dictionary_r_cost)
    return dictionary_r,dictionary_r_cost
    #return render(request, 'recommendation/recommendation.html',{'rec_rest':dictionary_r})


def recommendation_h(request):

    id = request.user.username

    rec_system_h = recommender_copy_h.RecommenderCopyH()

    # training
    print('\nTraining data:')
    print('-> Number of ratings:  %s' % len(rec_system_h.ratings_train.data))
    print('-> Number of distinct users:  %s' % len(np.unique(rec_system_h.ratings_train.row)))
    print('-> Number of distinct items:  %s' % len(np.unique(rec_system_h.ratings_train.col)))
    print('-> Number of latent factors:  %d' % (rec_system_h.num_user_factors))

    '''
    rec_system.train()

    print('\nLearned values:')
    print('\n-> User factors:')
    print(rec_system.user_factors)
    print('\n-> Item factors:')
    print(rec_system.item_factors)

    # testing
    print('\nTest data:')
    print('-> Number of ratings:  %s' % len(rec_system.ratings_test.data))
    print('-> Number of distinct users:  %s' % len(np.unique(rec_system.ratings_test.row)))
    print('-> Number of distinct items:  %s' % len(np.unique(rec_system.ratings_test.col)))

    test_rmse = rec_system.test()
    # test_rmse = rec_system.test_baseline()
    # test_rmse = rec_system.test_naive()

    print('\nRMSE: %s\n' % test_rmse)
    '''

    # rec_system.test_example()
    # recommendation of top items for a specific user
    user_id = id
    num_items = 20
    rec_system_h.recommend(user_id, num_items)
    rec_pre = rec_system_h.top_predictions
    rec_hotel = rec_system_h.top_rest_names
    rec_hotel_cost = rec_system_h.top_hotel_cost
    dictionary_h = dict(zip(rec_hotel, rec_pre))
    dictionary_h_cost = dict(zip(rec_hotel, rec_hotel_cost))
    print(dictionary_h)
    print(dictionary_h_cost)
    print("end of recommender_h")
    return dictionary_h,dictionary_h_cost
    #return render(request, 'recommendation/recommendationHotel.html', {'rec_hotel': dictionary_h})


def distancecalc(request):
    return render(request,'personal/distance_calc.html')

def dirdisplay(request):
    return render(request,'personal/directions.html')

def placedisplay(request):
    pid=''
    if request.method == 'POST' and 'b1' in request.POST:
        form = ContactForm(request.POST)

        if form.is_valid():
            pid = form.cleaned_data['name']
            with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\tourist_final1.json',
                      encoding='utf-8') as j_file:
             tFile = json.load(j_file)

            output_dict = [x for x in tFile if x['pid'] == pid]
            rec_rest,rec_rest_cost= recommendation_r(request)
            rec_hotel,rec_hotel_cost = recommendation_h(request)
            return render(request, 'personal/placedisplay.html',{'pdict':output_dict,'rec_rest':rec_rest,'rec_hotel':rec_hotel})
    else:
        return render(request,'personal/home.html')

def hoteldisplay(request):


    if request.method == 'POST' and 'b5' in request.POST:
        form = ImgForm(request.POST)

        if form.is_valid():
            pid = form.cleaned_data['name']
            imgsrc = form.cleaned_data['name1']
            with open('N:\\projectStart\\mysite\\webapp\\static\\datasets\\final_hotels1.json',
                      encoding='utf-8') as j_file:
             tFile = json.load(j_file)

            output_dict = [x for x in tFile if x['business_id'] == pid]
            print(output_dict)
            rec_rest,rec_rest_cost = recommendation_r(request)
            rec_hotel,rec_hotel_cost = recommendation_h(request)
            print(rec_hotel)
            print(rec_hotel_cost)
            return render(request, 'personal/hoteldisplay.html',{'pdict':output_dict,'rec_rest':rec_rest,'rec_hotel':rec_hotel,'imgsrc':imgsrc})
    else:
        return render(request,'personal/home.html')
def restdisplay(request):

    if request.method == 'POST' and 'b3' in request.POST:
        form = ImgForm(request.POST)

        if form.is_valid():
            pid = form.cleaned_data['name']
            imgsrc = form.cleaned_data['name1']
            with open('N:\\projectStart\\mysite\\webapp\\static\\datasets\\final_rest.json',
                      encoding='utf-8') as j_file:
             tFile = json.load(j_file)

            output_dict = [x for x in tFile if x['business_id'] == pid]
            rec_rest,rec_rest_cost = recommendation_r(request)
            rec_hotel,rec_hotel_cost = recommendation_h(request)
            return render(request, 'personal/restdisplay.html',{'pdict':output_dict,'rec_rest':rec_rest,'rec_hotel':rec_hotel,'imgsrc':imgsrc})
    else:
        return render(request,'personal/home.html')


def ratingsubmit(request):
    pid=''
    place=''
    rate=''
    hid=''
    rid=''
    if request.method == 'POST' and 'b7' in request.POST:
        form = RateSubmitForm(request.POST)
        uid = request.user.username
        if form.is_valid():
            pid=form.cleaned_data['name1']
            place= form.cleaned_data['name2']
            rate = form.cleaned_data['name3']
        ratedict={}
        ratedict['pid']=pid
        ratedict['place'] = place
        ratedict['star'] = rate
        ratedict['user_id'] = uid
        print(ratedict)
        with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\place_user_rating.json',encoding='utf-8') as f:
            rFile = json.load(f)
        rFile.insert(0,ratedict)
        with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\place_user_rating.json',mode='w', encoding='utf-8') as f:
            json.dump(rFile, f, sort_keys=True, indent=4, separators=(',', ': '))

    if request.method == 'POST' and 'b8' in request.POST:
        form = RateSubmitForm(request.POST)
        uid = request.user.username
        if form.is_valid():
            hid = form.cleaned_data['name1']
            place = form.cleaned_data['name2']
            rate = form.cleaned_data['name3']
        ratedict = {}
        ratedict['hid'] = hid
        ratedict['place'] = place
        ratedict['star'] = rate
        ratedict['user_id'] = uid
        print(ratedict)

        with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\hotel_user_rating.json',encoding='utf-8') as f:
            hFile = json.load(f)
        hFile.insert(0,ratedict)
        with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\hotel_user_rating.json',mode='w', encoding='utf-8') as f:
            json.dump(hFile, f, sort_keys=True, indent=4, separators=(',', ': '))


    if request.method == 'POST' and 'b9' in request.POST:
        form = RateSubmitForm(request.POST)
        uid = request.user.username
        if form.is_valid():
            rid = form.cleaned_data['name1']
            place = form.cleaned_data['name2']
            rate = form.cleaned_data['name3']
        ratedict = {}
        ratedict['rid'] = rid
        ratedict['place'] = place
        ratedict['star'] = rate
        ratedict['user_id'] = uid
        print(ratedict)

        with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\rest_user_rating.json',encoding='utf-8') as f:
            rFile = json.load(f)
        rFile.insert(0,ratedict)
        with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\rest_user_rating.json',mode='w', encoding='utf-8') as f:
            json.dump(rFile, f, sort_keys=True, indent=4, separators=(',', ': '))

    return render(request, 'personal/infodisplay.html')

def filter(request):
    rec_rest, rec_rest_cost = recommendation_r(request)
    rec_hotel, rec_hotel_cost = recommendation_h(request)
    if request.method == 'POST' and 'f1' in request.POST:
        x = dict((k, v) for k, v in rec_rest_cost.items() if v < 4000)
        sorted_x = sorted(x.items(), key=operator.itemgetter(1))
        sorted_rest_cost = dict(sorted_x)
        return render(request, 'personal/filters.html',{'rec_cost':sorted_rest_cost})
    if request.method == 'POST' and 'f2' in request.POST:
        x = dict((k, v) for k, v in rec_rest_cost.items() if 4000<=v < 6000)
        sorted_x = sorted(x.items(), key=operator.itemgetter(1))
        sorted_rest_cost = dict(sorted_x)
        return render(request, 'personal/filters.html', {'rec_cost': sorted_rest_cost})
    if request.method == 'POST' and 'f3' in request.POST:
        x = dict((k, v) for k, v in rec_rest_cost.items() if 6000<=v < 8000)
        sorted_x = sorted(x.items(), key=operator.itemgetter(1))
        sorted_rest_cost = dict(sorted_x)
        return render(request, 'personal/filters.html', {'rec_cost': sorted_rest_cost})
    if request.method == 'POST' and 'f4' in request.POST:
        x = dict((k, v) for k, v in rec_rest_cost.items() if v>8000)
        sorted_x = sorted(x.items(), key=operator.itemgetter(1))
        sorted_rest_cost = dict(sorted_x)
        return render(request, 'personal/filters.html', {'rec_cost': sorted_rest_cost})
    if request.method == 'POST' and 'f5' in request.POST:
        x = dict((k, v) for k, v in rec_hotel_cost.items() if v < 4000)
        sorted_x = sorted(x.items(), key=operator.itemgetter(1))
        sorted_hotel_cost = dict(sorted_x)
        return render(request, 'personal/filters.html', {'rec_cost': sorted_hotel_cost})
    if request.method == 'POST' and 'f6' in request.POST:
        x = dict((k, v) for k, v in rec_hotel_cost.items() if 4000<=v < 6000)
        sorted_x = sorted(x.items(), key=operator.itemgetter(1))
        sorted_hotel_cost = dict(sorted_x)
        return render(request, 'personal/filters.html', {'rec_cost': sorted_hotel_cost})
    if request.method == 'POST' and 'f7' in request.POST:
        x = dict((k, v) for k, v in rec_hotel_cost.items() if 6000<=v < 8000)
        sorted_x = sorted(x.items(), key=operator.itemgetter(1))
        sorted_hotel_cost = dict(sorted_x)
        return render(request, 'personal/filters.html', {'rec_cost': sorted_hotel_cost})
    if request.method == 'POST' and 'f8' in request.POST:
        x = dict((k, v) for k, v in rec_hotel_cost.items() if v>8000)
        sorted_x = sorted(x.items(), key=operator.itemgetter(1))
        sorted_hotel_cost = dict(sorted_x)
        return render(request, 'personal/filters.html', {'rec_cost': sorted_hotel_cost})
def nearbyrec(request):
    if request.method == 'POST' and 'btn1' in request.POST:
        form = ImgForm(request.POST)

        if form.is_valid():
            city = form.cleaned_data['name']
            state = form.cleaned_data['name1']
            with open('N:\\projectStart\\mysite\\webapp\\static\\datasets\\final_rest.json',
                      encoding='utf-8') as j_file:
                rFile = json.load(j_file)
            r_dis = [x for x in rFile if (x['city']==city)]
            r_dis=r_dis[:30]
            with open('N:\\projectStart\\mysite\\webapp\\static\\datasets\\final_hotels1.json',
                      encoding='utf-8') as j_file:
                hFile = json.load(j_file)
            h_dis = [x for x in hFile if (x['city'] == city)]
            h_dis=h_dis[:30]
            with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\tourist_final1.json',
                      encoding='utf-8') as j_file:
                pFile = json.load(j_file)
            p_dis = [x for x in pFile if (x['state_code']==state)]
            p_dis=p_dis[:6]
            return render(request, 'personal/nearbyrec.html', {'rest_near': r_dis,'hotel_near':h_dis,'place_near':p_dis})
    if request.method == 'POST' and 'btn2' in request.POST:
        form = ImgForm(request.POST)

        if form.is_valid():
            city = form.cleaned_data['name']
            state = form.cleaned_data['name1']
            with open('N:\\projectStart\\mysite\\webapp\\static\\datasets\\final_rest.json',
                      encoding='utf-8') as j_file:
                rFile = json.load(j_file)
            r_dis = [x for x in rFile if (x['state']==state)]
            r_dis=r_dis[:30]

            with open('N:\\projectStart\\mysite\\webapp\\static\\datasets\\final_hotels1.json',
                      encoding='utf-8') as j_file:
                hFile = json.load(j_file)
            h_dis = [x for x in hFile if (x['state'] == state)]
            h_dis=h_dis[:30]
            #print(h_dis)
            with open('N:\\projectStart\\mysite\\webapp\\static\\personal\\tourist_final1.json',
                      encoding='utf-8') as j_file:
                pFile = json.load(j_file)
            p_dis = [x for x in pFile if (x['state_code']==state)]
            p_dis=p_dis[:6]

            return render(request, 'personal/nearbyrec.html', {'rest_near': r_dis,'hotel_near':h_dis,'place_near':p_dis})
