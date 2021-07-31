import os
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    



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


    # In[11]:


    full_image = browser.links.find_by_partial_text("FULL IMAGE").click()
    html = browser.html
    soup = bs(html, 'html.parser')


    # In[12]:


    image_elem = soup.find("img", class_="fancybox-image").get("src")
    image_elem


    # In[13]:


    featured_image_url = image_url + image_elem
    featured_image_url


    # In[14]:


    facts_url = "https://galaxyfacts-mars.com/"


    # In[15]:


    facts_table = pd.read_html(facts_url)[0]


    # In[16]:


    facts_table


    # In[17]:


    facts_table.columns=facts_table.iloc[0]
    facts_table


    # In[18]:


    facts_table.set_index("Mars - Earth Comparison", inplace=True)
    facts_table


    # In[19]:


    facts_df = facts_table[1:].reset_index()
    facts_df


    # In[20]:


    facts_df.to_html()


    # In[21]:


    all_images_url = "https://marshemispheres.com/"
    browser.visit(all_images_url)


    # In[22]:


    html = browser.html
    soup = bs(html, 'html.parser')


    # In[23]:


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
        


    # In[24]:


    hemisphere_image_urls


    # In[25]:


    browser.quit()

