# The scrape file used in the app.py
# Based off the mission_to_mars.ipynb workbook
# 5 functions are defined.

import os
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import datetime as dt
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# This function brings all other function results together.
# It starts by establishing the splinter connection.
# All results from other functions are returned in a data dictionary.
# A timestamp stamp is also added into the dictionary.

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_para = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_para,
        "featured_image": space_image(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    browser.quit()

    return data


# This function scrapes the mars news title and paragraph.

def mars_news(browser):

    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')


    try:
        news_elem = soup.select_one('div.list_text')
        news_title = news_elem.find("div", class_="content_title").get_text()
        news_para = news_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_para


# This function scrapes the featured image.

def space_image(browser):

    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    try:

        full_image = browser.links.find_by_partial_text("FULL IMAGE").click()
        html = browser.html
        soup = bs(html, 'html.parser')

        image_elem = soup.find("img", class_="fancybox-image").get("src")
    
        featured_image_url = image_url + image_elem
  
    except AttributeError:
        return None
    
    return featured_image_url


# This function scrapes the mars facts table using the pandas read html method.
# Note the additional attributes adding into the facts_table.to_html line.
# These attributes create a nice looking table for the website.

def mars_facts():
    
    try:

        facts_url = "https://galaxyfacts-mars.com/"

        facts_table = pd.read_html(facts_url)[0]

        facts_table.columns=["Description", "Mars", "Earth"]

        facts_table.set_index("Description", inplace=True)
        facts_table = facts_table.drop(facts_table.index[[0]])
       
        facts_table_html = facts_table.to_html(justify="left", border="1", classes="table table-sm table-striped table-dark font-weight-light text-align-left", col_space='150px')

    except AttributeError:
        return None

    return facts_table_html


# This final function returns the mars hemispheres titles and url dictionary in a list.

def mars_hemispheres(browser):
    
    all_images_url = "https://marshemispheres.com/"
    browser.visit(all_images_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    try:
        hemisphere_divs = soup.find_all('div', class_="item")

        hemisphere_image_urls = []

        for hemisphere in range(len(hemisphere_divs)):
            
            hem_details = browser.find_by_css("img.thumb")
            hem_details[hemisphere].click()
            
            html = browser.html
            soup = bs(html, 'html.parser')
            
            title = browser.find_by_css("h2.title").first.value
            page_div = soup.find("div", class_="downloads")
            img_href = page_div.a["href"]
            
            img_url = all_images_url + img_href
            
            hemisphere_image_urls.append({"title": title, "img_url": img_url})
            
            browser.back()
    
    except AttributeError:
        return None

    return hemisphere_image_urls
