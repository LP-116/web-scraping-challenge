# Web Scraping Challenge
## Web Scraping Homework - Mission to Mars
---

### Task

This assignment contained two parts. The first part involved scraping 4 different websites using Jupyter Notebook, BeautifulSoup, Pandas and Splinter.
The second part involved using MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URL's in part 1.

---
### Method

#### Part 1

In part one 4 different URL's were visited.
The first URL was "https://redplanetscience.com/"
From this website the first News Title and Paragraph was extracted by using Splinter and BeautifulSoup (BS) . The BS methon _find_ was used with div and the  content_title class and article_teaser_body class to pull the information.

The second URL was "https://spaceimages-mars.com/".
From the website the full size image url was pulled by first finding the image link and then clicking in it.
Once the full image is displayed, the img source was found under the class "fancybox-image". The img source was then added to the base URL to give us the full image URL.

The third URL was "https://galaxyfacts-mars.com/" were the html was read in via pandas pd.read_html function.
The first table was stored and converted into html.

The last URL visited was https://marshemispheres.com/.
Here a for loop was used to enter each hemispher page and extract the title and full image URL.
find_by_css was used in the for loop, as I found it easier to identify the areas required. 
For a detailed explanation on how the loop is completed, please refer to the comments in the mission_to_mars jupyter notebook.

#### Part 2







---
### Result

The app.py file needs to be run in Python through the terminal. 
The app runs the scrape file which as previous discussed scrapes all the required data from each webpage.

The data is returned in an index.html file as per screen shot below.

<img src="https://user-images.githubusercontent.com/82348616/128123729-039ba458-9eae-4644-bb87-e59bbce05b68.PNG" width="500">




---
### Files
     
     
     
