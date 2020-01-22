import pandas as pd
import numpy as np
restaurants=pd.read_csv('restaurants2.csv')
ratings=pd.read_csv('rating_final.csv')
ratings.drop(['food_rating', 'service_rating'], axis=1, inplace=True)
#Create one data frame from the three
dataset = pd.merge(restaurants, ratings)


#print(restaurants.info())
#print(ratings.info())
#print(dataset.head())
ratings_total = dataset.groupby('name').size()
#print(ratings_total)
ratings_mean = (dataset.groupby('name'))['name','rating'].mean()
#print(ratings_mean.info())

#modify the dataframes so that we can merge the two
ratings_total = pd.DataFrame({'name':ratings_total.index, 'total_ratings': ratings_total.values})
ratings_mean['name'] = ratings_mean.index
#final merge
final = pd.merge(ratings_mean, ratings_total).sort_values(by = 'total_ratings',ascending= False)
#print(final)
#print(final.describe())
#final = final[:100].sort_values(by = 'rating',ascending = False)
final = final[:35].sort_values(by = 'rating',ascending = False)
print(final.head())
