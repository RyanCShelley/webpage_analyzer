
import advertools as adv
from advertools import crawl
import pandas as pd
from bs4 import BeautifulSoup
import requests
from collections import Counter
from string import punctuation
import streamlit as st

st.title('Webpage Structure Analyzer')

st.subheader('Upload a spread sheet of URLs')
st.caption('The .csv file must contain a header named URLs')

uploaded_file = st.file_uploader("Choose a file")

df = pd.read_csv(uploaded_file)

url_list = df["URLs"].values.tolist()

adv.crawl(url_list,
         output_file='list_crawl.jl',
         follow_links=False)

crawl_df = pd.read_json('list_crawl.jl', lines=True)

df = crawl_df[['url','title','meta_desc', "h1", "h2", "h3", "h4", "h5", "h6", 'img_alt', 'img_src']].copy()

st.write(df)

st.subheader('Check out your data!')

st.caption('Below is the list of URLs with imformation about the content structure.')


   


        
