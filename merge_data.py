# import libraries
import pandas as pd
import json

# preparing dataframe
df = pd.read_pickle('results/table.pkl')
columns = df.columns[:2]
df = df[columns]
df = df.rename(columns = {'movie_id':'id'})

movies = pd.read_csv('movie_dataset/tmdb_5000_movies.csv')
columns = ['id', 'genres', 'overview', 'release_date', 'vote_average']
movies = movies[columns]
movies = movies.merge(df, on ='id')

df = pd.read_csv('movie_dataset/tmdb_5000_credits.csv')
df = df.rename(columns = {'movie_id':'id', 'crew':'director'})
columns = ['id', 'cast', 'director']
df = df[columns]
movies = movies.merge(df, on ='id')

def extract_genres(data):
    if len(data)==0:
        return " "
    else:
        list=[]
        data = json.loads(data)
        for x in data:
            list.append(x['name'])
        return ', '.join(list)

def extract_casts(data):
    list = []
    data = json.loads(data)
    for x in data[3:]:
        list.append(x['name'])
    return ', '.join(list)

def extract_director(data):
    list =[]
    data = json.loads(data)
    for x in data:
        if x['job']=='Director':
            return x['name']

movies['genres'] = movies['genres'].apply(extract_genres)
movies['cast'] = movies['cast'].apply(extract_casts)
movies['director'] = movies['director'].apply(extract_director)


# save data
movies.to_pickle('results/final_table.pkl')