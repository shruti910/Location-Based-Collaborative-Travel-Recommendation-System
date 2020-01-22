import pandas as pd
import numpy as np
rest=pd.read_csv('dataset/restaurant.csv')
rating=pd.read_csv('dataset/rate.csv')
#print(rest.head())
rating.head()
def replace_name(x):
    return rest[rest['placeID']==x].name.values[0]
rating.placeID=rating.placeID.map(replace_name)
rating.head()
M=rating.pivot_table(index=['userID'],columns=['placeID'],values='rating')
M.shape
def pearson(s1,s2):
    s1_c=s1-s1.mean()
    s2_c=s2-s2.mean()
    return np.sum(s1_c*s2_c)/np.sqrt(np.sum(s1_c**2)*np.sum(s2_c**2))
#print(pearson(M['Kiku Cuernavaca'],M['El Rincon de San Francisco']))
def get_recs(rest_name,M,num):
    import numpy as np
    reviews=[]
    for name in M.columns:
        if name ==rest_name:
            continue
            cor=pearson(M[rest_name],M[name])
            if np.isnan(cor):
                continue
            else:
                reviews.append((name,cor))
        reviews.sort(key=lambda tup:tup[1],reverse=True)
        return reviews[:num]
recs=get_recs('Restaurante Pueblo Bonito',M,10)
print(recs[:10])
