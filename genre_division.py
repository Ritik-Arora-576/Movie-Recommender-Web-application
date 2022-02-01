# import libraries
import pickle as pkl

list = ['Action', 'Science Fiction', 'Comedy', 'Romance', 'Horror', 'Mystery', 'Crime']

with open('results/details.pkl','rb') as f:
    dict = pkl.load(f)

def get_movies(x):
    data = []
    for id in dict.keys():
        genres = dict[id]['genres'].split(", ")
        num = 0
        den = 0
        for genre in genres:
            if genre == x:
                num+=1
            if genre in list:
                den+=1
        ratio = num / (den + 1)
        data.append([id, ratio, dict[id]['vote_average']])

    data = sorted(data, key=lambda x:x[1], reverse=True)
    data = data[:500]
    data = sorted(data, key=lambda x:x[2], reverse=True)
    data = data[:50]

    for i in range(50):
        data[i] = [dict[data[i][0]]['title'], dict[data[i][0]]['poster_path'], data[i][0]]

    final_data = []
    for i in range(10):
        final_data.append(data[i*5:(i+1)*5])

    return final_data

genre_dict = {}

for ele in list:
    genre_dict[ele] = get_movies(ele)

with open('results/genres.pkl', 'wb') as f:
  pkl.dump(genre_dict, f)