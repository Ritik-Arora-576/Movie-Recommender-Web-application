# import liberaries
import numpy as np
import pandas as pd
import pickle as pkl
from fuzzywuzzy import process 
import requests
import json

# load data
with open('results/similar.pkl', 'rb') as f:
  similarity = pkl.load(f)

movie = pd.read_pickle('results/table.pkl')

def top_reccomended_movies(movie_name):
  result = process.extractOne(movie_name, movie['title'])
  movie_name = result[0]
  idx = movie[movie['title'] == movie_name].index
  sim = similarity[idx][0]
  sim = sorted(enumerate(sim), reverse=True, key = lambda x: x[1])[1:6]
  movie_list=[]
  for data in sim:
    idx = movie.iloc[data[0]]['movie_id']
    url = "https://api.themoviedb.org/3/movie/" + str(idx) + "?api_key=0b0436848e78c2a056025ebf0959366a&language=en-US"
    dict = requests.get(url)
    dict = json.loads(dict.text)
    base_img = "https://image.tmdb.org/t/p/w185/"
    if dict['poster_path']!=None:
      movie_list.append([dict['original_title'], base_img + dict['poster_path'], idx])
    else:
      movie_list.append([dict['original_title'], " ", idx])
    
  return movie_list

