# Importing Packages
import streamlit as st
import pandas as pd

from collections import Counter
from wordcloud import WordCloud

import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns


# Page configuration
st.set_page_config(
    page_title = 'Sentiment Analyzer',
    #page_icon = '',
    layout = 'wide'
)

# Logo and Title
a, b = st.columns([1, 10]) #setting columns
with a:
    st.text("")
    st.image("logo_official.png", width=50)
with b:
    st.title("Twitter Sentiment Analyzer")

# Loading dataset
@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv("sentiment_elon_demo.csv")

sentiment = get_data()

st.markdown("## Thema: Elon Musk")
st.markdown("### Sentiment: Trends")
# Columns for visualisations
fig_col_a, fig_col_b = st.columns(2)

with fig_col_a:
    data_agg = sentiment[['User ID','Datum','Label']].groupby(['Datum','Label']).count().reset_index()
    data_agg.columns = ['Datum','Label','counts']
    fig = px.line(data_agg, x='Datum', y='counts',color='Label', title='Sentiment über die Zeit')
    st.plotly_chart(fig, use_container_width=True)

with fig_col_b:
    fig = px.pie(data_agg, values='counts', names='Label', title='Sentiment kummuliert')
    st.plotly_chart(fig,use_container_width=True) 


# Loading Wordclouds

st.markdown("### Sentiment Wordclouds: Top Words")

# Importing dataset
@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv("text_demo.csv")

tweets = get_data()

# Visualisation
words_list = [word for line in tweets for word in line.split()]
word_counts = Counter(words_list).most_common(50)
words_df = pd.DataFrame(word_counts)
words_df.columns = ['word','frequency']
tweets_series = words_df.word
text_cloud = ' '.join(tweets_series)

wordcloud = WordCloud(background_color="white").generate(text_cloud)

fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### Sentiment: positive Wörter")
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)


with fig_col2:
    st.markdown("### Sentiment: negative Wörter")
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
    

st.markdown("Created by Aleksandra Klofat @datenverstehen.de")
