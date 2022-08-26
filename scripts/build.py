from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from joblib import dump
from pandas import read_csv

# reads "result_movies.csv" as pandas dataframe
movies = read_csv("data/result_movies.csv")

# convert a collection of text documents to a matrix of token counts.
cv = CountVectorizer(max_features=5000, stop_words="english")

# learn the vocabulary dictionary and return document-term matrix.
vector = cv.fit_transform(movies["tags"]).toarray()

# compute cosine similarity between samples in X and Y
similarity = cosine_similarity(vector)

# dumps model as a pickle files
dump(movies, open("models\movie_list.pkl", "wb"))
dump(similarity, open("models\similarity.pkl", "wb"))
