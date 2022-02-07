import streamlit as st
import requests
import pickle

API_KEY = '61cfe3074967b33e1cae3a5940277386'

movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_titles = movies_list['title'].values

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id, API_KEY)).json()
    return "https://image.tmdb.org/t/p/w500/" + response['poster_path'];

def recommend(movie_title, topk):
    df_movie = movies_list[movies_list['title'] == movie_title]
    if df_movie.shape[0] == 0:
        return None
    else:
        movie_index = df_movie.index[0]
        topk_movie_similarities = sorted(list(enumerate(similarity[movie_index])), key = lambda x: x[1], reverse=True)[1:topk+1]
        # fetch movie posters
        return zip([movies_list.iloc[item[0]]['title'] for item in topk_movie_similarities], [fetch_poster(movies_list.iloc[item[0]]['id']) for item in topk_movie_similarities])

st.title('Movie Recommender System')

selected_movie = st.selectbox('Select a movie title', movie_titles)

if st.button('Recommend'):
    recommended_movie_list = list(recommend(selected_movie, 5))
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(recommended_movie_list[0][1], caption=recommended_movie_list[0][0])
    with col2:
        st.image(recommended_movie_list[1][1], caption=recommended_movie_list[1][0])
    with col3:
        st.image(recommended_movie_list[2][1], caption=recommended_movie_list[2][0])
    with col4:
        st.image(recommended_movie_list[3][1], caption = recommended_movie_list[3][0])
    with col5:
        st.image(recommended_movie_list[4][1], caption=recommended_movie_list[4][0])
    


