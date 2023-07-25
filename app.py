import streamlit as st
import pickle
import pandas as pd
import requests
import feather

st.title('Movie Recommender System')

# Load the pickled data directly as a DataFrame
movies = pickle.load(open('movies.pkl', 'rb'))

movies_similarity = feather.read_dataframe('df_similarity_data.feather')


def fetch_movie_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8'.format(movie_id))
    data = response.json()
    print("poster path: " + "https://image.tmdb.org/t/p/w500/" + data['poster_path'])
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend_similar_movies(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    similarity_dist_for_a_movie = movies_similarity[movie_index]
    sorted_movie_list = sorted(list(enumerate(similarity_dist_for_a_movie)), reverse=True, key=(lambda x: x[1]))[1:6]
    top_five_movies = []
    top_five_movies_posters = []
    for i in sorted_movie_list:
        movie_details = movies.iloc[i[0]]
        top_five_movies.append(movie_details.title)
        top_five_movies_posters.append(fetch_movie_poster(movie_details.movie_id))
    return top_five_movies, top_five_movies_posters


selected_movie_name = st.selectbox('Search for the movie to get top 5 recommended movies', movies['title'].values)

if st.button('Recommend'):
    movies, posters = recommend_similar_movies(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5, gap="medium")
    with col1:
        st.text(movies[0])
        st.image(posters[0])
    with col2:
        st.text(movies[1])
        st.image(posters[1])
    with col3:
        st.text(movies[2])
        st.image(posters[2])
    with col4:
        st.text(movies[3])
        st.image(posters[3])
    with col5:
        st.text(movies[4])
        st.image(posters[4])
