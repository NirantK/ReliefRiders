# st.write(data.columns)
# st.dataframe(data)
from copy import deepcopy

import pandas as pd
import streamlit as st
from haversine import haversine

st.title("Find Closest Relief Rider")


@st.cache(ttl=3600)
def load_data(
    url="https://docs.google.com/spreadsheets/d/e/2PACX-1vR17ZMSIIDqLKh9YZC2poBM7ts-sP8Psntdg--zo8F5Tb2TfMzZ9AawaY4_x2rVP4nNZgI5ULFNZtpl/pub?gid=521576028&single=true&output=csv",
):
    df = pd.read_csv(url)
    try:
        location_column_name = "GPS Coordinates of your location or Nearest Landmark"
        df = df.rename(columns={location_column_name: "Location"})
    except KeyError as ke:
        raise Exception(f"Did not find {location_column_name}.\n{ke}")

    # Location Format Conversion
    df[["lat", "lon"]] = df["Location"].str.split(",", expand=True)
    df.lat = df.lat.astype(float)
    df.lon = df.lon.astype(float)

    # Filter Data
    df = df[df.Status == "Active"]
    df = df.drop(
        columns=[
            "RIDER ID",
            "Status",
            "Blood",
            "emergency",
            "basket",
            "email address",
            "gender",
        ]
    )
    return df


# Load data and make a copy
data = load_data()

df = deepcopy(data)
# st.dataframe(df)

# Input
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

# Compute
def get_distance(row):
    loc = (row["lat"], row["lon"])
    dist = haversine(help_loc, loc)
    # st.write(dist)
    return dist


# Main Data Render
def sort_and_display(df: pd.DataFrame, rider_count: int):
    df["Distance"] = df.apply(get_distance, axis=1)
    sorted_df = df.sort_values(by="Distance", ascending=True)
    sorted_df.set_index("Name of Relief Rider", inplace=True)
    cols = sorted_df.columns.tolist()
    columns = ["Distance", "Phone Number", "Area Covered"] + cols[2:-4]
    sorted_df = sorted_df[columns]
    return sorted_df[:rider_count]


st.table(sort_and_display(df, rider_count=rider_count))
