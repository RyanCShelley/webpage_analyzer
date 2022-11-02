import pandas as pd
from bs4 import BeautifulSoup
import requests
from collections import Counter
from string import punctuation
import streamlit as st
import urllib
import pandas as pd
import numpy as np
from requests_html import HTML
from requests_html import HTMLSession
import random


user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
url = 'https://httpbin.org/headers'
for i in range(1,4):
#Pick a random user agent
    user_agent = random.choice(user_agent_list)
#Set the headers 
    headers = {'User-Agent': user_agent}
#Make the request
    response = requests.get(url,headers=headers)


st.title('Webpage Structure Analyzer')

st.subheader('Review the structure of the pages in the top ten')

query = st.text_input("Put Your Target Keyword Here", value="Add Your Keyword")


def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response 
    except requests.exceptions.RequestException as e:
        print(e)
       
def scrape_google(query):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)
    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links

def get_results(query):
    
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query)
    
    return response

def parse_results(response):
    
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".IsZvec"
    
    results = response.html.find(css_identifier_result)

    output = []
    
    for result in results:

        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'url': result.find(css_identifier_link, first=True).attrs['href']
        }
        
        output.append(item)
        
    return output


def google_search(query):
    response = get_results(query)
    return parse_results(response)

if query is not None:
    results = google_search(query)
    df = pd.DataFrame(results)



def get_img_cnt(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.content)
	return len(soup.find_all('img'))

number_images = []

# Loop items in results
for url in df['url']:
	TotalImages = get_img_cnt(url) 
	if TotalImages is not None: # assuming the download was successful
		number_images.append(TotalImages)
df["number images"] = number_images

def get_h_cnt(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.content)
	h1 = len(soup.find_all('h1'))
	h2 = len(soup.find_all('h2'))
	h3 = len(soup.find_all('h3'))
	h4 = len(soup.find_all('h4'))
	h5 = len(soup.find_all('h5'))
	h6 = len(soup.find_all('h6'))
	return h1+h2+h3+h4+h5+h6

def get_h1_cnt(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.content)
	h1 = len(soup.find_all('h1'))
	return h1

def get_h2_cnt(url):
  	response = requests.get(url)
  	soup = BeautifulSoup(response.content)
  	h2 = len(soup.find_all('h2'))
  	return h2

def get_h3_cnt(url):
  	response = requests.get(url)
  	soup = BeautifulSoup(response.content)
  	h3 = len(soup.find_all('h3'))
  	return h3

def get_h4_cnt(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.content)
	h4 = len(soup.find_all('h4'))
	return h4

def get_h5_cnt(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.content)
	h5 = len(soup.find_all('h5'))
	return h5

def get_h6_cnt(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.content)
	h6 = len(soup.find_all('h6'))
	return h6

total_num_headers = []

for url in df['url']:
	TotalHeaders = get_h_cnt(url) 
	if TotalHeaders is not None: # assuming the download was successful
		total_num_headers.append( TotalHeaders)
df["total number headers"] = total_num_headers

num_h1 = []

for url in df['url']:
  	h1 = get_h1_cnt(url) 
  	if h1 is not None: # assuming the download was successful
  		num_h1.append(h1)
df["number of h1"] = num_h1
	
num_h2 = []

for url in df['url']:
	h2 = get_h2_cnt(url) 
	if h2 is not None: # assuming the download was successful
		num_h2.append(h2)
df["number of h2"] = num_h2

num_h3 = []

for url in df['url']:
	h3 = get_h3_cnt(url) 
	if h3 is not None: # assuming the download was successful
		num_h3.append(h3)
df["number of h3"] = num_h3

num_h4 = []

for url in df['url']:
	h4 = get_h4_cnt(url) 
	if h4 is not None: # assuming the download was successful
		num_h4.append(h4)
df["number of h4"] = num_h4
	
num_h5 = []

for url in df['url']:
	h5 = get_h5_cnt(url) 
	if h5 is not None: # assuming the download was successful
		num_h5.append(h5)
df["number of h5"] = num_h5

num_h6 = []

for url in df['url']:
	h6 = get_h6_cnt(url) 
	if h6 is not None: # assuming the download was successful
		num_h6.append(h6)
df["number of h6"] = num_h6

def get_word_cnt(url):
  res = requests.get(url)
  html_page = res.content
  soup = BeautifulSoup(html_page, 'html.parser')
  text = soup.find_all(text=True)
  output = ''
  blacklist = [
    '[document]',
    'noscript',
    'header',
    'html',
    'meta',
    'head', 
    'input',
    'script',
    'style']
  for t in text:
    if t.parent.name not in blacklist:
      output += '{} '.format(t)
  output = output.strip()
  output = output.replace('\n','')
  word_list = output.split()
  number_of_words = len(word_list)
  return number_of_words

word_count = []

for url in df['url']:
	wordcount = get_word_cnt(url) 
	if  wordcount is not None: # assuming the download was successful
		word_count.append(wordcount)
		
df["word count"] = word_count


st.subheader('Check out your data!')

st.caption('Below is the list of URLs with imformation about the content structure.')

st.write(df)

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='serp_df.csv',
    mime='text/csv',
)

st.subheader('Word Count')

st.bar_chart(data=df, x="url", y="word count", use_container_width=True)

st.subheader('Total Number of Headers')

st.bar_chart(data=df, x="url", y="total number headers", use_container_width=True)

st.subheader('Total Number of Images')

st.bar_chart(data=df, x="url", y="number images", use_container_width=True)

