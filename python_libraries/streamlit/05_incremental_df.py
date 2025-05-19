
# This exapmles shows how to increment a dataframe every time a button is pressed
import streamlit as st
import SessionState
import pandas as pd

st.header("Grow table of movies and related words clicking a button")

movies = []
words = []

ss = SessionState.get(movies=movies, words=words)

container_movies = st.container()
container_words = st.container()

new_movie = container_movies.text_input('Write here movie to add')
new_words = container_movies.text_input('Write here related words to movie (separated by a comma)')
add_button = container_words.button('add')

if add_button:
    if new_movie in ss.movies:
        st.write(f'{new_movie} already in the table')
    else:
        ss.movies.append(new_movie)
        ss.words.append(new_words.split(','))

#st.write('movies:')
#st.write(ss.movies)
#st.write('words:')
#st.write(ss.words)

st.header("Table")

movies = ss.movies
words = ss.words
df = pd.DataFrame({'movie': movies, 'words': words})
st.dataframe(df)
