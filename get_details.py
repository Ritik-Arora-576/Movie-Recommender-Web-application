# import libraries
import pandas as pd
import requests
import json
import pickle as pkl

def details(idx, df):
    id = df.iloc[idx]['id']
    dict = {}
    dict['genres'] = df.iloc[idx]['genres']
    dict['overview'] = df.iloc[idx]['overview']
    dict['release_date'] = df.iloc[idx]['release_date']
    dict['vote_average'] = df.iloc[idx]['vote_average']
    dict['title'] = df.iloc[idx]['title']
    dict['cast'] = df.iloc[idx]['cast']
    dict['director'] = df.iloc[idx]['director']

    url = "https://api.themoviedb.org/3/movie/" + \
        str(id) + "?api_key=0b0436848e78c2a056025ebf0959366a&language=en-US"
    x = requests.get(url)
    x = json.loads(x.text)
    base_img = "https://image.tmdb.org/t/p/w185/"

    if 'poster_path' in x and x['poster_path']!=None:
        dict['poster_path'] = base_img + x['poster_path']
    else:
        dict['poster_path'] = " "

    if 'homepage' in x and x['homepage']!=None:
        dict['homepage'] = x['homepage']
    else: 
        dict['homepage'] = ' '

    return dict

super_dict = {}
df = pd.read_pickle('results/final_table.pkl')

for idx in range(df.shape[0]):
    super_dict[df.iloc[idx]['id']] = details(idx,df)

with open('results/details.pkl', 'wb') as f:
  pkl.dump(super_dict, f)