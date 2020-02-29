# Import Dependecies 
import pymongo
from bs4 import BeautifulSoup as bs
from splinter import Browser
from pymongo import MongoClient
import pandas as pd 
import requests 


    
  
mars_info = {}

# Mars News
def scrape_all():
    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    martian_data = {
        "mars_news" : scrape_mars_news(browser),
        "Featured Image" : scrape_mars_image(browser),
        "Mars Weather" : scrape_mars_weather(browser),
        "mars_facts" : scrape_mars_facts(browser),
        "Mars Hemispheres" : scrape_mars_hemispheres(browser)
    }

    browser.quit()

    return martian_data

def scrape_mars_news(browser):
        # Mars News
      
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        html = browser.html

        soup = BeautifulSoup(html, 'html.parser')

        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        mars_info['news-title'] = news_title
        mars_info['news_paragraph']  = news_p
        return mars_info

        #browser.quit()

def scrape_mars_image(browser):

        # Featured Image
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)

        html_image = browser.html

        soup = BeautifulSoup(html_image, 'html.parser')

        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        main_url = 'https://www.jpl.nasa.gov'

        featured_image_url = main_url + featured_image_url

        featured_image_url 

        mars_info['featured_image_url'] = featured_image_url

        return mars_info

        #browser.quit()

def scrape_mars_weather(browser):
        
        # Mars Weather 
        
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        html_weather = browser.html

        soup = BeautifulSoup(html_weather, 'html.parser')

        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

        for tweet in latest_tweets: 
            weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else: 
                pass

        mars_info['weather_tweet'] = weather_tweet

        return mars_info

        #browser.quit()

def scrape_mars_facts(browser):
        
        # Mars Facts

        facts_url = 'http://space-facts.com/mars/'

        mars_df = pd.read_html(facts_url)[0]

        data = mars_df.to_html(classes="table")

        mars_info['mars_facts'] = data
        
        return mars_info
        
        #browser.quit()

def scrape_mars_hemispheres(browser):

        # Mars Hempispheres

        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        html_hemispheres = browser.html

        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        items = soup.find_all('div', class_='item')

        mars_images = []

        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop
        for i in items: 
            
            title = i.find('h3').text
            
            partial_img = i.find('a', class_='itemLink product-item')['href']
            
            browser.visit(hemispheres_main_url + partial_img)
            
            partial_img = browser.html
            
            soup = BeautifulSoup( partial_img, 'html.parser')
            
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            mars_images.append({"title" : title, "img_url" : img_url})

        mars_info['mars_images'] = mars_images

        #return mars_info

        #browser.quit()

        '''

        mars_info = {
            "news_title": news_title, 
            "news_p": news_p,
            "featured_image_url": featured_image_url, 
            "weather_tweet": weather_tweet, 
            "mars_facts": data, 
            "mars_images": mars_images,
        }

        #browser.quit()
        
        return mars_info'''
    
# create connection to mongo db
#client = pymongo.MongoClient('mongodb://localhost:27017/mars_app')
#db = client.planets_db
#db.mars.drop()
#insert record to mongo db
#db.mars.insert_one(mars_info)
