# Import Libraries
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup

import requests

import pandas as pd
import html5lib

import pymongo

# Initialize Browser
def init_browser():
	executable_path = {'executable_path': './plugins/chromedriver.exe'}
	return Browser('chrome', **executable_path, headless=False)

### Create seperate function for each collection to the website:

# Finds the latest news and discoveries regarding Mars
def latest_mars_news():

	# request response from Mars url
	url = "https://mars.nasa.gov/news/"
	response = requests.get(url=url)

	# Make beautifulsoup object, parse with html
	soup = BeautifulSoup(
	    markup=response.text,
	    features="html.parser"
	)

	# Inspecting Page, Title is in <div class="content_title"> & body is in <div class="article_teaser_body">
	results = soup.find_all("div", class_="slide")

	# take only the latest result:
	result = results[0]

	title = result.find("div", class_="content_title").get_text().strip()
	description = result.find("div", class_="rollover_description_inner").get_text().strip()

	# Store results in a dictionary:
	latest = {
		"title":title,
		"description":description
	}

	# return results: 
	return latest

# Finds the featured image on JPL for Mars
def jpl_mars_image():

	# Use chromedriver and assign to browser
	browser = init_browser()

	url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(url)

	# Scrape from url using beautifulsoup object
	html = browser.html
	soup = BeautifulSoup(html, "html.parser")
	image = soup.find("a", class_="button fancybox")["data-fancybox-href"]

	# define full url for image
	url = "https://www.jpl.nasa.gov"
	image_url = url + image

	# Quit broswer session
	browser.quit()

	return image_url

# Finds the most updated weather on Mars
def mars_weather():

	# Use mars twitter account to find the latest weather updates
	url = "https://twitter.com/marswxreport?lang=en"
	response = requests.get(url=url)

	soup = BeautifulSoup(
	    markup=response.text,
	    features="html.parser"
	)

	weather = soup.find(
	    "p",
	    class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"
	).get_text().strip()

	return weather

# Finds various facts regarding Mars
def mars_facts():

	# Use Pandas to pull in table of mars facts.
	url = "https://space-facts.com/mars/"
	tables = pd.read_html(url, flavor="html5lib")
	# define the dataframe as the first table in the tables list
	facts_df = tables[0]

	# clean dataframe and return to function call
	facts_df.rename(columns={0: "parameter", 1:"value"}, inplace=True)
	facts_df.set_index("parameter", inplace=True)
	return facts_df

# Finds images for each hemisphere on Mars
# Currently not working due to too many requests.
def mars_hemispheres():

	# Use chromedriver and assign to browser.
	browser = init_browser()

	url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(url)

	# Find all the hemispeheres from the url:
	html = browser.html
	soup = BeautifulSoup(html, "html.parser")
	hemis = soup.find_all("div", class_="item")

	# Define empty list to append image urls to
	hemisphere_image_urls = []

	# for loop to append empty list with each Hemisphere Header and image url
	for hemi in hemis: 
	    
	    # extract title, and click on page by title text
	    title = hemi.find("h3").get_text().strip()
	    browser.click_link_by_partial_text(title)
	    
	    # redefine temporary beautiful soup object for new page
	    html_temp = browser.html
	    soup_temp = BeautifulSoup(html_temp, "html.parser")
	    
	    # find image, and define image_url
	    image = soup_temp.find("img", class_="wide-image")["src"]
	    image_url = browser.url + image
	    
	    # create dictionary of results and append to image url list
	    product_dict = {
	        "title":title,
	        "image_url":image_url
	    }
	    hemisphere_image_urls.append(product_dict)
	    
	    # Go back to previous page to restart the loop
	    browser.back()

	return hemisphere_image_urls
