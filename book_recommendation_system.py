# -*- coding: utf-8 -*-
"""book recommendation system.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aQ3t9FNpGX4SFlVFGNlHat0Tdger3ItI
"""

import numpy as np
import pandas as pd

users=pd.read_csv('/content/sample_data/Users.csv')
books=pd.read_csv('/content/sample_data/Books.csv')
ratings=pd.read_csv('/content/sample_data/Ratings.csv')

books

print(books.shape)
print(users.shape)
print(ratings.shape)

users.isnull().sum() ##age has lot of missing values

"""we are going to build a popularity based recommender system"""

#we now merge ratings and books based on their common field isbn
ratings_and_names=ratings.merge(books,on='ISBN')

#we need to group by book title and we check book title with highest rating
num_rating =ratings_and_names.groupby('Book-Title').count()['Book-Rating'].reset_index()
num_rating.rename(columns={'Book-Rating':'num_rating'},inplace=True)
num_rating

#now we need to find the avg rating to find the best rated movies
avg_num_rating =ratings_and_names.groupby('Book-Title').mean()['Book-Rating'].reset_index()
avg_num_rating.rename(columns={'Book-Rating':'avg_rating'},inplace=True)
avg_num_rating

popular_df=(num_rating.merge(avg_num_rating,on='Book-Title'))
popular_df

#we r only going to consider the first 50 movies that have a rating over 250
popular_df=popular_df[popular_df['num_rating']>=250].sort_values('avg_rating',ascending =False).head(50)
popular_df

popular=popular_df.merge(books,on='Book-Title').drop_duplicates('Book-Title')[['Book-Title','num_rating','avg_rating','Book-Author','Image-URL-M']]
popular.shape

"""collaborative filtering based recommender system
(here we will take into consideration people who have voted for more that 200 books and books that have more than 50 ratings)
"""

x=ratings_and_names.groupby('User-ID').count()['Book-Rating']>200
readers=x[x].index#gets value of people who have voted for more than 200 books
users_filtered=ratings_and_names[ratings_and_names['User-ID'].isin(readers)]

y=users_filtered.groupby('Book-Title').count()['Book-Rating']>50
famous_books=y[y].index#gets value of books with more that 50 ratings
books_filtered=users_filtered[users_filtered['Book-Title'].isin(famous_books)]
books_filtered

#The pivot table function takes in a data frame and the parameters detailing the shape you want the data to take. Then it outputs summarized data in the form of a pivot table



pt=books_filtered.pivot_table(index='Book-Title',columns='User-ID',values='Book-Rating')

pt=pt.fillna(0)
pt

"""now we have separated the user and book ratings . now we can use this data to calculate and find similar books"""

from sklearn.metrics.pairwise import cosine_similarity

"""all the book values are compared with all the other book values to find their closest neighhbour"""

similarity_score =cosine_similarity(pt)
similarity_score.shape

"""we now need to create a recommend function that recommends 5 most similar books based on the distance"""

np.where(pt.index=='Zoya')[0][0]

def recommend(book_name):
  #fetch index postions
  #here we take index along with distance score and then we sort it and then we take the first 5 values .we take it in decending oreder
  similar_items=sorted(list(enumerate(similarity_score[0])),key=lambda x:x[1],reverse=True)[1:6]
  for i in similar_items:
    print(pt.index[i[0]])

recommend('1984')