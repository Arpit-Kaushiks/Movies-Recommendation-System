import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_date(movie_id):
    release_date = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    date = release_date.json()
    return date['release_date']
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_date = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)

        #fetch release date
        recommended_movies_date.append(fetch_date(movie_id).split('-')[0])

        # fetch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_date,recommended_movies_poster


movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movies Recommendation System')

selected_movie_name = st.selectbox('Enter a movies name',movies['title'].values)

if st.button('Recommend',key='Enter'):
    names,date,poster = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.text("("+date[0]+")")
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.text("(" + date[1] + ")")
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.text("(" + date[2] + ")")
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.text("(" + date[3] + ")")
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.text("(" + date[4] + ")")
        st.image(poster[4])
