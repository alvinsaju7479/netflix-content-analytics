import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Netflix Analytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)
df = pd.read_csv("../outputs/netflix_cleaned.csv")
st.markdown("""
# 🎬 Netflix Content Analytics Dashboard

### Global Content Trends & Business Insights
""")
with st.expander("📄 View Dataset"):
    st.dataframe(df)
col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "🎬 Total Titles",
    len(df)
)

col2.metric(
    "🎥 Movies",
    (df["type"]=="Movie").sum()
)

col3.metric(
    "📺 TV Shows",
    (df["type"]=="TV Show").sum()
)

country_count = (
    df["country"]
      .dropna()
      .str.split(", ")
      .explode()
      .nunique()
)

col4.metric(
    "🌍 Countries",
    country_count
)
st.sidebar.header("Filters")
country = st.sidebar.selectbox(
    "Country",
    ["All"] + sorted(df["country"].dropna().unique())
)
rating = st.sidebar.multiselect(
    "Rating",
    df["rating"].dropna().unique(),
    default=df["rating"].dropna().unique()
)
content = st.sidebar.multiselect(
    "Content Type",
    df["type"].unique(),
    default=df["type"].unique()
)
year = st.sidebar.slider(
    "Release Year",
    int(df.release_year.min()),
    int(df.release_year.max()),
    (
        int(df.release_year.min()),
        int(df.release_year.max())
    )
)
title = st.sidebar.text_input(
    "Search Title"
)
filtered = df.copy()

if country != "All":
    filtered = filtered[
        filtered["country"] == country
    ]

filtered = filtered[
    filtered["rating"].isin(rating)
]

filtered = filtered[
    filtered["type"].isin(content)
]

filtered = filtered[
    filtered["release_year"].between(year[0],year[1])
]

if title:
    filtered = filtered[
        filtered["title"].str.contains(title,case=False)
    ]
left,right = st.columns(2)
with left:

    fig = px.pie(
        filtered,
        names="type",
        title="Movies vs TV Shows",
        hole=.55
    )

    st.plotly_chart(fig,use_container_width=True)
with right:

    growth = filtered.release_year.value_counts().sort_index()

    fig = px.area(
        x=growth.index,
        y=growth.values,
        title="Content Growth"
    )

    st.plotly_chart(fig,use_container_width=True)
left,right = st.columns(2)
genre = (
    filtered["listed_in"]
      .str.split(", ")
      .explode()
      .value_counts()
      .head(10)
)

fig = px.bar(
    x=genre.values,
    y=genre.index,
    orientation="h",
    color=genre.values
)
st.plotly_chart(fig, use_container_width=True)
country = (
    filtered["country"]
      .dropna()
      .str.split(", ")
      .explode()
      .value_counts()
      .head(10)
)

fig = px.bar(
    x=country.values,
    y=country.index,
    orientation="h",
    color=country.values
)
left,right = st.columns(2)
template="plotly_dark"
st.subheader("Filtered Dataset")

st.dataframe(filtered)
