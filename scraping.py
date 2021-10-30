#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Executables
    executable_path = {'executable_path':ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = True)
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(browser),
        "last_modifed": dt.datetime.now(),
        "hemispheres": hemisphere_urls(browser)
    }

    #Stop webdriver and return data
    browser.quit()
    return data



def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')
        
        # Use the parent element to find title and paragraph texts
        news_title = slide_elem.find('div', class_="content_title").text
        news_p = slide_elem.find('div', class_="article_teaser_body").text
    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# ### A collection of Mars facts in table format

# Visit URL
def mars_facts(browser):
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    try:
        #Use 'read_html' to scrape the facts table into dataframe
        df = pd.read_html(url)[0]

    except BaseException:
        return None

    # Assign columns and seting index of dataframe
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace =True)
    
    # Convert dataframe into HTML format. 
    return df.to_html()

def hemisphere_urls(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    hemisphere_image_urls = []

    for i in range(0,4):
        browser.find_by_tag('h3')[i].click()
        html = browser.html 
        hemi_soup = soup(html, 'html.parser')
        img_url_rel = hemi_soup.find('ul').find('a')['href']
        hemi_img_url = f"{url}{img_url_rel}"
        hemi_title = hemi_soup.find('h2', class_='title').text
        hemisphere = {
            'title': hemi_title,
            'img_url': hemi_img_url
        }
        hemisphere_image_urls.append(hemisphere)
        browser.back()

    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())