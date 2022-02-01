# importing some libraries
import numpy as np
import pandas as pd
import os
import warnings
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import pickle as pkl

# use to ignore the warnings
warnings.filterwarnings("ignore")

# fetching the csv file from a folder
folder_path = 'movie_dataset'
credits = pd.read_csv(os.path.join(folder_path, 'tmdb_5000_credits.csv'))
movies = pd.read_csv(os.path.join(folder_path, 'tmdb_5000_movies.csv'))

# merge two dataframes into a single dataframe
movie = movies.merge(credits, on = 'title')

# extract out the nessesary columns from a table
columns = ['movie_id', 'title', 'cast', 'crew', 'genres', 'overview', 'keywords']
movie = movie[columns]

# drop the columns which contains the null value
movie.dropna(inplace = True)

def into_list(data):
  # as data in a string format which contains list of dictionary so list(eval) is used to convert string into list of dictionary format
  data = list(eval(data))
  arr =[(x['name'].replace(" ","")).lower() for x in data]
  return arr

def cast_into_list(data):
  data = list(eval(data))
  # we are considering top 4 casts
  arr =[(x['name'].replace(" ","")).lower() for x in data[:4]]
  return arr

def crew_into_list(data):
  data = list(eval(data))
  # we are considering only director in a crew
  for x in data:
    if x['job']=='Director':
      return (x['name'].replace(" ","")).lower()

# apply the changes
movie['keywords'] = movie['keywords'].apply(into_list)
movie['genres'] = movie['genres'].apply(into_list)
movie['cast'] = movie['cast'].apply(cast_into_list)
movie['crew'] = movie['crew'].apply(crew_into_list)

movie.dropna(inplace = True)

# creating the tags for every movie
def create_tags(df):
  genres = " ".join(df['genres'])
  keywords = " ".join(df['keywords'])
  cast = " ".join(df['cast'])
  overview = df['overview'].lower()
  crew = df['crew']
  return " ".join([overview, genres, keywords, cast, crew])

list = []
for idx in range(movie.shape[0]):
  list.append(create_tags(movie.iloc[idx]))
movie['tags'] = list

# extracted out some important columns
columns = ['movie_id', 'title', 'tags']
movie = movie[columns]

# in order to convert similar kinds of words into one word we use stemming
def stemming(text):
  ps = PorterStemmer()
  list=[]
  for word in text.split(" "):
    list.append(ps.stem(word))
  return " ".join(list)

# apply stemming on every text in a tag column
movie['tags'] = movie['tags'].apply(stemming)

# convert all the tags into vector matrix with 8500 features
vectorize = CountVectorizer(max_features = 5000, stop_words = 'english')
vector = vectorize.fit_transform(movie['tags']).toarray()

# now find the cosine distance from every vectors to other vectors
# at high dimension data euclidean distance method fails so we use cosine distance to get the better performance
similarity = cosine_similarity(vector)

# converting the similarity matrix into numpy array and save it in results folder
similarity = np.array(similarity)

with open('results/similar.pkl', 'wb') as f:
  pkl.dump(similarity, f)

# save the movie dataframe
movie.to_pickle('results/table.pkl')