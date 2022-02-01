# import libraries
from audioop import reverse
import pickle as pkl

with open('results/details.pkl','rb') as f:
    dict = pkl.load(f)

def top_rated():
    data = []
    for idx in dict.keys():
        data.append([idx, dict[idx]['vote_average']])
    data = sorted(data, reverse = True, key=lambda x:x[1])

    # pick out the top rated 150 movies 
    data = data[:150]

    for i in range(150):
        data[i] = [dict[data[i][0]]['title'], dict[data[i][0]]['poster_path'], data[i][0]]

    final_data = []
    for i in range(30):
        final_data.append(data[i*5:(i+1)*5])

    return final_data

data = top_rated()

with open('results/top_rated.pkl', 'wb') as f:
  pkl.dump(data, f)