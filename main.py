from flask import Flask, render_template, request
from reccomender import top_reccomended_movies
import pickle as pkl

app = Flask(__name__)

@app.route("/home")
def hello():
    return render_template("home.html")

@app.route("/results", methods=["POST", "GET"])
def results():
    if request.method == "POST":
        movie = request.form['movie_name']
        movie = top_reccomended_movies(movie)

    return render_template("result.html", movies = movie)

@app.route('/<int:id>')
def details(id):
    with open('results/details.pkl', 'rb') as f:
        dict = pkl.load(f)
    return render_template("details.html", data = dict[id])

@app.route('/<string:genre>')
def genres(genre):
    if genre=="Scifi":
        genre = "Science Fiction"
    with open('results/genres.pkl','rb') as f:
        dict = pkl.load(f)
    return render_template("genre.html", list = dict[genre])

@app.route('/top_rated')
def top():
    with open('results/top_rated.pkl','rb') as f:
        data = pkl.load(f)
    return render_template('genre.html', list = data)

app.run(debug=True)