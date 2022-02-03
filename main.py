from flask import Flask, render_template, request, redirect, session
from reccomender import top_reccomended_movies
import pickle as pkl
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def login():
    if 'name' in session:
        return redirect('/home')
    return render_template("login.html")

@app.route('/create')
def create():
    return render_template("SignUp.html")

@app.route('/check_login', methods=['POST'])
def check_login():
    with open('database/users.pkl', 'rb') as f:
        dict = pkl.load(f)
    email = request.form['email']
    password = request.form['password']
    if (email in dict) and (dict[email][1]==password):
        session['name']=dict[email][0]
        return redirect('/home')
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    with open('database/users.pkl', 'rb') as f:
        dict = pkl.load(f)
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    conf_password = request.form['conf_password']

    if (email not in dict) and (password == conf_password):
        dict[email] = [name, password]
        with open('database/users.pkl', 'wb') as f:
            pkl.dump(dict, f)
        return redirect('/')
    return redirect('/create')

@app.route('/logout')
def logout():
    session.pop('name')
    return redirect('/')

@app.route("/home")
def hello():
    if 'name' in session:
        return render_template("home.html", name =session['name'])
    return redirect('/')

@app.route("/results", methods=["POST", "GET"])
def results():
    if 'name' in session:
        if request.method == "POST":
            movie = request.form['movie_name']
            movie = top_reccomended_movies(movie)

        return render_template("result.html", movies = movie, name =session['name'])
    return redirect('/')

@app.route('/<int:id>')
def details(id):
    if 'name' in session:
        with open('results/details.pkl', 'rb') as f:
            dict = pkl.load(f)
        return render_template("details.html", data = dict[id], name =session['name'])
    return redirect('/')

@app.route('/<string:genre>')
def genres(genre):
    if 'name' in session:
        if genre=="Scifi":
            genre = "Science Fiction"
        with open('results/genres.pkl','rb') as f:
            dict = pkl.load(f)
        return render_template("genre.html", list = dict[genre], name =session['name'])
    return redirect('/')

@app.route('/top_rated')
def top():
    if 'name' in session:
        with open('results/top_rated.pkl','rb') as f:
            data = pkl.load(f)
        return render_template('genre.html', list = data, name =session['name'])
    return redirect('/')

app.run(debug=True)