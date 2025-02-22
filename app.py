import streamlit as st
import pandas as pd
import time


def read_recommend_files():
    df = pd.read_csv("data_filter.csv")
    df_rd = pd.read_csv("recommend_description.csv")
    df_rdc = pd.read_csv("recommend_director_cast.csv")

    return df, df_rd, df_rdc

df, df_rd, df_rdc = read_recommend_files()
selected_column = "0"


def get_name(film_index):
    result = dict(df.loc[film_index, ["Title", "Poster", "Genre", "Hybrid_Score"]])
    result["Index"] = film_index
    return result

def get_recommend_rd(film_column):
    get_rd = df_rd[film_column].values.tolist()
    return get_rd

def get_recommend_rdc(film_column):
    get_rdc = df_rdc[film_column].values.tolist()
    return get_rdc



st.set_page_config(page_title="Movie Recommendation", layout="wide", page_icon="snake")
st.title("Movie Recommendation :snake:")

tab_content , tab_da = st.tabs(["Content","Director & Actor"])

with st.sidebar:
    st_select_film = st.selectbox("Select a movie", options=[get_name(i) for i in range(len(df))], format_func=lambda x: x["Title"])
    with st.spinner("Wait for it..."):
        time.sleep(3)
        st.text(st_select_film["Title"])
        st.image(st_select_film["Poster"], use_container_width=True)
        st.empty()
        st.write(f"Genre : {st_select_film['Genre']}")
        st.write(f"Score : {round(st_select_film['Hybrid_Score'],1)} / :star:")
        selected_column = str(st_select_film["Index"])


rd_list = get_recommend_rd(selected_column)
rdc_list = get_recommend_rdc(selected_column)


with tab_content:
    for index, col in enumerate(st.columns(5)):
        with col:
            result = get_name(rd_list[index])
            st.write(result["Title"])
            st.image(result["Poster"])

    st.empty()

    for index, col in enumerate(st.columns(5)):
        with col:
            result = get_name(rd_list[index + 5])
            st.write(result["Title"])
            st.image(result["Poster"])


with tab_da:
    for index, col in enumerate(st.columns(5)):
        with col:
            result = get_name(rdc_list[index])
            st.write(result["Title"])
            st.image(result["Poster"])

    st.empty()

    for index, col in enumerate(st.columns(5)):
        with col:
            result = get_name(rdc_list[index + 5])
            st.write(result["Title"])
            st.image(result["Poster"])