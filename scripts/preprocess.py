import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import ast  # process trees of the Python abstract syntax grammar


def convert(text):
    """
    Safely evaluate the given expression

    Args:
        text (str): required string

    Returns:
        List: list of evaluate words
    """
    return [x["name"] for x in ast.literal_eval(text)]


def fetch_director(text):
    """
    Safely evaluate the given expression if the job is Director

    Args:
        text (str): required string

    Returns:
        List: list of evaluate words
    """
    return [x["name"] for x in ast.literal_eval(text) if x["job"] == "Director"]


def collapse(text):
    """
    Removes spaces from the given sentence text

    Args:
        text (str): required string

    Returns:
        List: list of separated words
    """
    return [x.replace(" ", "") for x in text]


# reads movies.csv & credits.csv as pandas dataframe
movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# merge two dataframes together using "title" column
movies = movies.merge(credits, on="title")

# select required columns only
movies = movies[["movie_id", "title", "overview", "genres", "keywords", "cast", "crew"]]

# drop NaN values from the dataframe
movies.dropna(inplace=True)

# apply convert function for the genres, keywords & cast columns
movies["genres"] = movies["genres"].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)
movies["cast"] = movies["cast"].apply(convert)

# apply lambda function to get the first 3 index of the string
movies["cast"] = movies["cast"].apply(lambda x: x[:3])

# apply fetch_director function for the crew column
movies["crew"] = movies["crew"].apply(fetch_director)

# apply collapse function for the genres, keywords, cast & crew columns
movies["cast"] = movies["cast"].apply(collapse)
movies["crew"] = movies["crew"].apply(collapse)
movies["genres"] = movies["genres"].apply(collapse)
movies["keywords"] = movies["keywords"].apply(collapse)

# apply lambda function to get the splitted words from the sentences
movies["overview"] = movies["overview"].apply(lambda x: x.split())

# creates a new column named "tags" to store the combined values of specified columns
movies["tags"] = (
    movies["overview"]
    + movies["genres"]
    + movies["keywords"]
    + movies["cast"]
    + movies["crew"]
)

# drop unwanted columns from the dataframe
movies.drop(columns=["overview", "genres", "keywords", "cast", "crew"], inplace=True)

# apply lambda function to join all the words
movies["tags"] = movies["tags"].apply(lambda x: " ".join(x))

# saves the resultant dataframe as csv file
movies.to_csv("data/result_movies.csv")
