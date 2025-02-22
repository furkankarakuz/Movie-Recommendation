import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 100)


def read_data(file="imdb-movies-dataset.csv"):
    dataframe = pd.read_csv(file)
    return dataframe

def weighted_sorting_score(dataframe, w1=0.6, w2=0.4):
    dataframe["Rating_Scaled"] = MinMaxScaler(feature_range=(1, 10)). fit(dataframe[["Rating"]]).transform(dataframe[["Rating"]])
    dataframe["Review_Scaled"] = MinMaxScaler(feature_range=(1, 10)).fit(dataframe[["Review Count"]]).transform(dataframe[["Review Count"]])
    dataframe["Hybrid_Score"] = (dataframe["Rating_Scaled"] * w1) + (dataframe["Review_Scaled"] * w2)

    dataframe = dataframe[dataframe["Hybrid_Score"] > 4]
    return dataframe


def prepare_dataset(dataframe):
    dataframe = dataframe[dataframe["Year"] >= 1990]

    dataframe["Director_Cast"] = dataframe["Director"] + ", " + dataframe["Cast"]
    dataframe["Director_Cast"] = dataframe["Director_Cast"].str.replace(" ", "").str.replace(",", " ")

    dataframe["Review Count"] = dataframe["Review Count"].str.replace(".", "").str.replace(",", "")
    dataframe["Review Count"] = dataframe["Review Count"].astype(float)

    dataframe["Review Count"].fillna(dataframe["Review Count"].mean(), inplace=True)
    dataframe["Rating"].fillna(dataframe["Rating"].mean(), inplace=True)
    dataframe = weighted_sorting_score(dataframe)

    dataframe.dropna(subset=["Genre", "Description", "Director", "Cast"], inplace=True)
    dataframe.drop(["Year", "Certificate", "Metascore", "Director", "Cast", "Review Title", "Review", "Review Count", "Rating", "Duration (min)"], axis=1, inplace=True)

    return dataframe.reset_index(drop=True)


def transform_column(dataframe, tfidf, column):
    dataframe['Description'] = dataframe[column].fillna('')
    tfidf_matrix = tfidf.fit_transform(dataframe[column])
    return tfidf_matrix


def calculate_cosine_sim(dataframe, column):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = transform_column(dataframe, tfidf, column)

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim


def content_based_recommender(title, cosine_sim, dataframe):
    indices = pd.Series(dataframe.index, index=dataframe['Title'])
    indices = indices[~indices.index.duplicated(keep='last')]
    movie_index = indices[title]
    similarity_scores = pd.DataFrame(cosine_sim[movie_index], columns=["score"])
    movie_indices = similarity_scores.sort_values("score", ascending=False)[1:11].index
    return dataframe['Title'].iloc[movie_indices]


dataframe = prepare_dataset(read_data())
cosine_sim_description = calculate_cosine_sim(dataframe, "Description")
cosine_sim_director_cast = calculate_cosine_sim(dataframe, "Director_Cast")

dataframe = dataframe[["Title", "Poster", "Genre", "Hybrid_Score"]]
dataframe.to_csv("data_filter.csv", index=False)




#content_based_recommender("Spider-Man", cosine_sim_description, dataframe)
#content_based_recommender("Spider-Man", cosine_sim_director_cast, dataframe)

data_description = {}
for i in range(len(dataframe)):
    data_description[i] = content_based_recommender(dataframe.iloc[i]["Title"],cosine_sim_description, dataframe).index.tolist()
pd.DataFrame(data_description).to_csv("recommend_description.csv", index=False)


data_director_cast = {}
for i in range(len(dataframe)):
    data_director_cast[i] = content_based_recommender(dataframe.iloc[i]["Title"], cosine_sim_director_cast, dataframe).index.tolist()
pd.DataFrame(data_director_cast).to_csv("recommend_director_cast.csv", index=False)


pd.read_csv("recommend_description.csv").head()