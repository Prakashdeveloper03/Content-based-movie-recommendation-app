from joblib import load
import streamlit as st
import requests

# setting app's title, icon & layout
st.set_page_config(page_title="Movie Recommender", page_icon="🎯")

# css style to hide footer, header and main menu details
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# loads saved models
movies = load(open("models/movie_list.pkl", "rb"))
similarity = load(open("models/similarity.pkl", "rb"))

# list of movie names
movie_list = movies["title"].values


def fetch_poster(movie_id):
    """
    Returns the movie poster url for the given movie id

    Args:
        movie_id (int): movie id number

    Returns:
        string: movie poster image url
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data["poster_path"]
    return f"https://image.tmdb.org/t/p/w500/{poster_path}"


def recommend(movie):
    """
    Returns recommended movies names & their posters

    Args:
        movie (str): movie name

    Returns:
        tuple[List]: returns list of movies names & their poster urls
    """
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1]
    )
    recommended_movie_names = []
    recommended_movie_posters = []
    for idx in distances[1:6]:
        movie_id = movies.iloc[idx[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[idx[0]].title)
    return recommended_movie_names, recommended_movie_posters


def main():
    st.header("Movie Recommender System")  # sets header text
    # shows all available movie names
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown", movie_list
    )
    if st.button("Recommend"):
        # calls the recommend() -> to get recommended movie names & posters list
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        col1, col2, col3, col4, col5 = st.columns(5)
        # every columns shows a recommended movie name & it's poster respectively
        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])
        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])
        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])


if __name__ == "__main__":
    main()  # calls the main()
