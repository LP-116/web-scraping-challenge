import os
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import datetime as dt
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


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

def mars_facts():
    
    try:

        facts_url = "https://galaxyfacts-mars.com/"

        facts_table = pd.read_html(facts_url)[0]

        facts_table.columns=["Description", "Mars", "Earth"]

        facts_table.set_index("Description", inplace=True)
       
        facts_table_html = facts_table.to_html(justify="left", border="2", classes="table table-sm table-striped table-info font-weight-light text-align-left", col_space='150px')

    except AttributeError:
        return None

    return facts_table_html


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
