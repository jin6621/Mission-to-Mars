#!/usr/bin/env python
# coding: utf-8

# In[172]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[173]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless = False)


# In[154]:


# Visit the mars nasa news site
url = 'http://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time = 1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
new_title = slide_elem.find('div', class_ = 'content_title').get_text()
new_title


# In[5]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').text
news_p


# ### Featured Images

# In[11]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[7]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[8]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[9]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_ = 'fancybox-image').get('src')
img_url_rel


# In[10]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[40]:


df = pd.read_html('https://galaxyfacts-mars.com/')[0]
df.columns = ['description','Mars','Earth']
df.set_index('description', inplace=True)
df


# In[45]:


df.to_html()


# In[46]:


browser.quit()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# ### Hemispheres

# In[164]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[190]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in range(3,7):
    
    #Title
    hem_soup = soup(browser.html)
    title = hem_soup.find_all('h3')[i-3].get_text()
    
    #Clicking into website for high-resolution image url
    full_img_elem = browser.find_by_tag('img')[i].click()
    html = browser.html
    img_soup = soup(html, 'html.parser')
    urls = img_soup.find_all('a')

    #URL is in position 3
    url = urls[3]['href']
    complete_url = f'https://marshemispheres.com/{url}'
    
    hemispheres = {
        "img_url": complete_url,
        "title":title
    }
    
    hemisphere_image_urls.append(hemispheres)
    
    browser.back()


# In[192]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[193]:


# 5. Quit the browser
browser.quit()


# #### ----- Testing ----- please disregard below

# In[156]:


hem_soup = soup(browser.html)


# In[ ]:


# Getting fourth image and title name. 
full_image = browser.find_by_tag('button')[1]
full_image.click()
url = hem_soup.find_all('img', class_ = "thumb")[3].get('src')
img_url = f'https://marshemispheres.com/{url}'
print(img_url)

title = hem_soup.find_all('h3')[3].get_text()
print(title)


# In[ ]:


# Need to loop through 3-6, and then position 3


# In[ ]:


hem_soup.find_all('h3')[3].get_text()


# In[131]:


# position 3 ~ 6
full_img_elem = browser.find_by_tag('img')[3].click()
html = browser.html
img_soup = soup(html, 'html.parser')
urls = img_soup.find_all('a')

#position 3
url = urls[3]['href']
complete_url = f'https://marshemispheres.com/{url}'
print(complete_url)


# In[133]:


# position 4 
full_img_elem = browser.find_by_tag('img')[4].click()
html = browser.html
img_soup = soup(html, 'html.parser')
urls = img_soup.find_all('a')

#position 3
url = urls[3]['href']
complete_url = f'https://marshemispheres.com/{url}'
print(complete_url)


# In[135]:


# Needs to broswer back. 
browser.back()


# In[183]:


hem_soup = soup(browser.html)
hem_soup.find_all('h3')[0].get_text()


# In[184]:


url = 'https://marshemispheres.com/'

browser.visit(url)
hem_soup = soup(browser.html)
title = hem_soup.find_all('h3')[0].get_text()
    
    #Clicking into website for high-resolution image url
full_img_elem = browser.find_by_tag('img')[3].click()
html = browser.html
img_soup = soup(html, 'html.parser')
urls = img_soup.find_all('a')

    #URL is in position 3
url = urls[3]['href']
complete_url = f'https://marshemispheres.com/{url}'
    
hemi = {
    "img_url": complete_url,
    "title":title
 }
    
print(hemi)
    
browser.back()


# In[185]:


url = 'https://marshemispheres.com/'

browser.visit(url)
hem_soup = soup(browser.html)
title = hem_soup.find_all('h3')[1].get_text()
    
    #Clicking into website for high-resolution image url
full_img_elem = browser.find_by_tag('img')[4].click()
html = browser.html
img_soup = soup(html, 'html.parser')
urls = img_soup.find_all('a')

    #URL is in position 3
url = urls[3]['href']
complete_url = f'https://marshemispheres.com/{url}'
    
hemi = {
    "img_url": complete_url,
    "title":title
 }
    
print(hemi)
    
browser.back()


# In[ ]:




