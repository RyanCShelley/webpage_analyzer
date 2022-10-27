
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
df['title'] = df['title'].str.replace('@@',', ')
df['meta_desc'] = df['meta_desc'].str.replace('@@',', ')
df['h1'] = df['h1'].str.replace('@@',', ')
df['h2'] = df['h2'].str.replace('@@',', ')
df['h3'] = df['h3'].str.replace('@@',', ')
df['h4'] = df['h4'].str.replace('@@',', ')
df['h5'] = df['h5'].str.replace('@@',', ')
df['h6'] = df['h6'].str.replace('@@',', ')
df['img_alt'] = df['img_alt'].str.replace('@@',', ')

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
	df["number_images"] = number_images

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
	df["total_number_headers"] = total_num_headers

num_h1 = []

for url in df['url']:
  	h1 = get_h1_cnt(url) 
  	if h1 is not None: # assuming the download was successful
  		num_h1.append(h1)
  	df["number_h1"] = num_h1
	
num_h2 = []

for url in df['url']:
	h2 = get_h2_cnt(url) 
	if h2 is not None: # assuming the download was successful
		num_h2.append(h2)
		df["number_h2"] = num_h2

num_h3 = []

for url in df['url']:
	h3 = get_h3_cnt(url) 
	if h3 is not None: # assuming the download was successful
		num_h3.append(h3)
	df["number_h3"] = num_h3

num_h4 = []

for url in df['url']:
	h4 = get_h4_cnt(url) 
	if h4 is not None: # assuming the download was successful
		num_h4.append(h4)
		df["number_h4"] = num_h4
	
num_h5 = []

for url in df['url']:
	h5 = get_h5_cnt(url) 
	if h5 is not None: # assuming the download was successful
		num_h5.append(h5)
		df["number_h5"] = num_h5

num_h6 = []

for url in df['url']:
	h6 = get_h6_cnt(url) 
	if h6 is not None: # assuming the download was successful
		num_h6.append(h6)
		df["number_h6"] = num_h6

def get_word_cnt(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.content)
	text_p = (''.join(s.findAll(text=True))for s in soup.findAll('p'))
	c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))
	text_div = (''.join(s.findAll(text=True))for s in soup.findAll('div'))
	c_div = Counter((x.rstrip(punctuation).lower() for y in text_div for x in y.split()))
	total = c_div + c_p
	words = len(total)
	return words

word_count = []

for url in df['url']:
	wordcount = get_word_cnt(url) 
	if  wordcount is not None: # assuming the download was successful
		word_count.append(wordcount)
		df["word_count_new"] = word_count

df['title'] = df['title'].str.replace('@@',' ')
df['meta_desc'] = df['meta_desc'].str.replace('@@',' ')
df['h1'] = df['h1'].str.replace('@@',' ')
df['h2'] = df['h2'].str.replace('@@',' ')
df['h3'] = df['h3'].str.replace('@@',' ')
df['h4'] = df['h4'].str.replace('@@',' ')
df['h5'] = df['h5'].str.replace('@@',' ')
df['h6'] = df['h6'].str.replace('@@',' ')
df['img_alt'] = df['img_alt'].str.replace('@@',' ')

st.write(df)

st.subheader('Check out your data!')

st.caption('Below is the list of URLs with imformation about the content structure.')


   


        
