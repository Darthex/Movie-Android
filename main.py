import pandas as pd
from flask import Flask, render_template, request, jsonify, make_response
import requests


def finalname(obj):
    String = obj
    a = String.replace(',', "")
    b = a.split()
    if b[-1] == "The":
        b.pop()
        return "The " + " ".join(b)

    else:
        return String


def format1(obj):
    String2 = obj
    a = String2.lower()
    b = a.split()
    if b[0] == "the":
        b.remove("the")
        return ' '.join(b) + ", the"

    else:
        return a


app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    v1 = request.json['movie-name1']
    v2 = request.json['movie-name2']
    v3 = request.json['movie-name3']
    v4 = request.json['movie-name4']
    v5 = request.json['movie-name5']

    vv1 = format1(v1)
    vv2 = format1(v2)
    vv3 = format1(v3)
    vv4 = format1(v4)
    vv5 = format1(v5)

    r1 = int(request.json['rating1'])
    r2 = int(request.json['rating2'])
    r3 = int(request.json['rating3'])
    r4 = int(request.json['rating4'])
    r5 = int(request.json['rating5'])

    print(v1, v2, v3, v4, v5, r1, r2, r3, r4, r5)
    movies_df = pd.read_csv('C:/Users/mrhar/Downloads/moviedataset/ml-latest/movie_lower.csv', encoding='iso-8859-1')

    # Cleaning Data
    movies_df['year'] = movies_df.title.str.extract('(\(\d\d\d\d\))', expand=False)
    movies_df['year'] = movies_df.year.str.extract('(\d\d\d\d)', expand=False)
    movies_df['title'] = movies_df.title.str.replace('(\(\d\d\d\d\))', '')
    movies_df['title'] = movies_df['title'].apply(lambda x: x.strip())
    movies_df['genres'] = movies_df.genres.str.split('|')

    # Making GenreTable where 1 means true and 0 means false
    moviesWithGenres_df = movies_df.copy()
    for idx, row in movies_df.iterrows():
        for genre in row['genres']:
            moviesWithGenres_df.at[idx, genre] = 1

    moviesWithGenres_df = moviesWithGenres_df.fillna(0)
    moviesWithGenres_df.head()

    # Getting User Input
    userInput = [
        {'title': vv1, 'rating': r1},
        {'title': vv2, 'rating': r2},
        {'title': vv3, 'rating': r3},
        {'title': vv4, 'rating': r4},
        {'title': vv5, 'rating': r5}
    ]

    # Making a user input movie table
    inputMovies = pd.DataFrame(userInput)
    inputId = movies_df[movies_df['title'].isin(inputMovies['title'].tolist())]
    inputMovies = pd.merge(inputId, inputMovies)
    inputMovies = inputMovies.drop('genres', 1).drop('year', 1)

    # Making a user input GenreTable
    userMovies = moviesWithGenres_df[moviesWithGenres_df['movieId'].isin(inputMovies['movieId'].tolist())]
    userMovies.head()
    userMovies = userMovies.reset_index(drop=True)
    userGenreTable = userMovies.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)

    # Actual code lmao
    userProfile = userGenreTable.transpose().dot(inputMovies['rating'])
    genreTable = moviesWithGenres_df.set_index(moviesWithGenres_df['movieId'])
    genreTable = genreTable.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)

    # Final Recommendations
    recommendationTable_df = ((genreTable * userProfile).sum(axis=1)) / (userProfile.sum())
    recommendationTable_df = recommendationTable_df.sort_values(ascending=False)

    new = movies_df.loc[movies_df['movieId'].isin(recommendationTable_df.head(20).keys())]
    result = new['title'].iat[0]

    name = finalname(result)
    fname = name.replace(" ", "+")
    print(fname)
    api = 'http://www.omdbapi.com/?t=' + fname + '&apikey=9ce2b137'
    print(api)
    response = requests.get(api)
    df = response.json()
    print(df)
    title = df["Title"]
    poster = df["Poster"]

    jsonResult = jsonify({"title": title, "src": poster})
    print(jsonResult)
    return jsonResult


if __name__ == '__main__':
    app.run(debug=True)
