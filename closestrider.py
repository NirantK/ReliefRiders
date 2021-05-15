from numpy import expand_dims, float64
from numpy.core.fromnumeric import sort
import streamlit as st
import pandas as pd
from haversine import haversine

st.title("Find Closest Relief Rider")


@st.cache
def load_data(
    url="https://docs.google.com/spreadsheets/d/e/2PACX-1vR17ZMSIIDqLKh9YZC2poBM7ts-sP8Psntdg--zo8F5Tb2TfMzZ9AawaY4_x2rVP4nNZgI5ULFNZtpl/pub?gid=2123468107&single=true&output=csv",
):
    df = pd.read_csv(url)
    columns_of_interest = [
        "Area",
        "Name of Relief Rider",
        "Phone number",
        "ACTIVE",
        "Location",
    ]
    try:
        df["Location"] = df["DO NOT FILL - GPS"]
        df = df[columns_of_interest]
    except KeyError as ke:
        raise Exception(f"Expected the titles to be {columns_of_interest}.\n{ke}")
    df[["lat", "lon"]] = df["Location"].str.split(",", expand=True)
    # st.text(df.dtypes)
    # df.lat = pd.to_numeric(df.lat)
    # df.lon = pd.to_numeric(df.lon)
    df.lat = df.lat.astype(float)
    df.lon = df.lon.astype(float)
    df = df[df.ACTIVE == "Yes"]
    # st.text(df.dtypes)
    return df


# st.dataframe(df)
help_input = st.text_input(
    label="Request Location",
    value="13.064058531224338, 77.58758101599165",
    help="Enter lat, lon as comma separated value",
)
help_loc = help_input.split(",")
lat = float(help_loc[0].strip())
lon = float(help_loc[1].strip())
help_loc = (lat, lon)

rider_count = 20
st.subheader(f"Your {rider_count} Closest riders are:")


def get_distance(row):
    loc = (row["lat"], row["lon"])
    dist = haversine(help_loc, loc)
    # st.write(dist)
    return dist


data = load_data()
from copy import deepcopy

df = deepcopy(data)
# st.dataframe(df)
df["dist"] = df.apply(get_distance, axis=1)
# st.dataframe(df)
sorted_df = df.sort_values(by="dist", ascending=True)
st.table(sorted_df[:rider_count])
