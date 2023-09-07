'''
Author: Mkothm
Email: mkothman.jr@gmail.com
'''

import pickle
import streamlit as st
import numpy as np
import os  # Import os to check file existence

st.header('Book Recommender System Using Machine Learning')

# Checking if the pickle files exist before attempting to open them
model_path = 'artifacts/model.pkl'
book_names_path = 'artifacts/book_names.pkl'
final_rating_path = 'artifacts/final_rating.pkl'
book_pivot_path = 'artifacts/book_pivot.pkl'

if not (os.path.exists(model_path) and os.path.exists(book_names_path) and
        os.path.exists(final_rating_path) and os.path.exists(book_pivot_path)):
    st.error("One or more pickle files do not exist. Please make sure all required files are available.")
else:
    # If all files exist, proceed with loading them
    model = pickle.load(open(model_path, 'rb'))
    book_names = pickle.load(open(book_names_path, 'rb'))
    final_rating = pickle.load(open(final_rating_path, 'rb'))
    book_pivot = pickle.load(open(book_pivot_path, 'rb'))
def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]: 
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['image_url']
        poster_url.append(url)

    return poster_url



def recommend_book(book_name):
    books_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6 )

    poster_url = fetch_poster(suggestion)
    
    for i in range(len(suggestion)):
            books = book_pivot.index[suggestion[i]]
            for j in books:
                books_list.append(j)
    return books_list , poster_url       



selected_books = st.selectbox(
    "Type or select a book from the dropdown",
    book_names
)

if st.button('Show Recommendation'):
    recommended_books,poster_url = recommend_book(selected_books)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_books[1])
        st.image(poster_url[1])
    with col2:
        st.text(recommended_books[2])
        st.image(poster_url[2])

    with col3:
        st.text(recommended_books[3])
        st.image(poster_url[3])
    with col4:
        st.text(recommended_books[4])
        st.image(poster_url[4])
    with col5:
        st.text(recommended_books[5])
        st.image(poster_url[5])