import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    response=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data =response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
    
movies_df=pickle.load(open('movies.pkl', 'rb'))
movies_list=movies_df['title'].values

similarity=pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

def recommend(movie):
    movie_index= movies_df[movies_df['title']==movie].index[0]
    distance= similarity[movie_index]
    movie_indices=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters=[]
    for i in movie_indices:
        movie_id=movies_df.iloc[i[0]].movie_id
        recommended_movies.append(movies_df.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

selected_movie_name = st.selectbox("Type or select a movie from the dropdown", movies_list)

if st.button('Recommend'):
    names,posters=recommend(selected_movie_name)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        col.text(names[idx])
        col.image(posters[idx])