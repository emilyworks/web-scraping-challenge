
import pandas as pd
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import pymongo
import requests


def scrape():
    # start a browser session
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    url = "https://redplanetscience.com/"
    browser.visit(url)


    html = browser.html
    soup = bs(html, "html.parser")


    # scrape and save in variables the latest news title and the associated news paragraph
    news_title = soup.find('div', class_='content_title').text

    news_p = soup.find('div', class_= 'article_teaser_body').text

    # close session
    browser.quit()


    #start a new session
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    nasa_img = 'https://spaceimages-mars.com'
    browser.visit(nasa_img)

    img_html = browser.html
    soup = bs(img_html, "html.parser")

    # scrape the img url link and save in variable
    featured_image_url = soup.find('img', class_='headerimage fade-in')
    featured_image_url = "https://spaceimages-mars.com/" + str(featured_image_url['src'])

    browser.quit()


    # scrape the mars facts page with pandas

    mars_facts_url = 'https://galaxyfacts-mars.com/'

    mars_facts = pd.read_html(mars_facts_url)[0]

    mars_facts = mars_facts.iloc[1:]

    mars_facts = mars_facts.rename(columns={0: '', 1: 'Mars', 2: 'Earth'})

    mars_facts = mars_facts.set_index('')

    mars_facts_html = mars_facts.to_html(classes="table")


    # set up for a browser session later on
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # find the hemisphere image urls

    mars_urls = ['https://marshemispheres.com/cerberus.html','https://marshemispheres.com/schiaparelli.html','https://marshemispheres.com/syrtis.html','https://marshemispheres.com/valles.html']

    hemisphere_img_dict = []

    for url in mars_urls:
        
        browser.visit(url)

        html = browser.html
        soup = bs(html, 'html.parser')
        
        title = soup.find('h2', class_='title').text
        href = soup.find('a', text='Sample').get('href')
        
        hem = {'title': title, 'image_url': "https://marshemispheres.com/" + str(href)}
        hemisphere_img_dict.append(hem)

    # close session    
    browser.quit()

    mars_info = {
            'news': news_title,
            'news_p': news_p,
            'featured_image_url': featured_image_url,
            'mars_facts': mars_facts_html,
            'hemispheres': hemisphere_img_dict
        }

    return mars_info
