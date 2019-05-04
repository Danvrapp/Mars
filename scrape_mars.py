from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import pymongo

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/Users/Dan/Desktop/CWRU/Web/Mongo/splinter/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)

def scrape_info():
    browser = init_browser()

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    browser.visit(url)
    # Scrape page into Soup
    html = browser.html
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(html, 'html.parser')
    
    time.sleep(1)

    # Retrieve the parent divs for all articles
    result = soup.find('li', class_="slide")
    mars_title=result.h3.text
    mars_blurb=result.a.text

    # URL of page to scrape image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Retrieve page 
    browser.visit(url)
    html = browser.html
    # Create BeautifulSoup object; parse with 'html'
    soup = BeautifulSoup(html, 'html.parser')
    
    results = soup.find('img', class_="thumb")
    img_results = 'https://www.jpl.nasa.gov' + results['src']

    # Twitter scrape for daily weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(html, 'html.parser')

    result = soup.find('p', class_="TweetTextSize")
    mars_weather = result.text
    
    # Get Mars facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    Mars_df = tables[0]
    Mars_df.columns = ['Attribute', 'Value']
    Mars_df.set_index('Attribute')
    Mars_html_table = Mars_df.to_html()
    Mars_df.to_html('Mars_table.html')
    #print (Mars_html_table)
    
    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
    {"title": "Cerberus Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
    ]

    hemi_1_img = hemisphere_image_urls[0]["img_url"]
    hemi_1_name = hemisphere_image_urls[0]["title"]
    hemi_2_img = hemisphere_image_urls[1]["img_url"]
    hemi_2_name = hemisphere_image_urls[1]["title"]
    hemi_3_img = hemisphere_image_urls[2]["img_url"]
    hemi_3_name = hemisphere_image_urls[2]["title"]
    hemi_4_img = hemisphere_image_urls[3]["img_url"]
    hemi_4_name = hemisphere_image_urls[3]["title"]

    # Store data in a dictionary
    mars_data = {
        "mars_news":mars_title,
        "mars_blurb":mars_blurb,
        "mars_img":img_results,
        "mars_weather":mars_weather,
        "mars_table":Mars_html_table,
        "hemi_1_img":hemi_1_img,
        "hemi_2_img":hemi_2_img,
        "hemi_3_img":hemi_3_img,
        "hemi_4_img":hemi_4_img,
        "hemi_1_title":hemi_1_name,
        "hemi_2_title":hemi_2_name,
        "hemi_3_title":hemi_3_name,
        "hemi_4_title":hemi_4_name
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
