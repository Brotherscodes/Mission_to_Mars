# Import the needed dependencies:
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# set the executable path and initialize the browser:
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# set up the html parser:
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_button = browser.find_by_tag('button')[1]
full_image_button.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# Find the relative image url
img_rel_url = img_soup.find('img', class_='fancybox-image').get('src')

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_rel_url}'

# ### Scaping full table with Pandas into a DataFrame:

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)

# Update your app.py to include this new df we made: # We can add by adding this exact output of code to
# our app:
df.to_html()

# Always tell your browser to quit when youre done to close the browser:
browser.quit()

## Copying the mission_to_mars_starter_code to complete step # 2, deliverable # 1:

## Import Splinter, BeautifulSoup, and Pandas
# from splinter import Browser
# from bs4 import BeautifulSoup as soup
# import pandas as pd
# from webdriver_manager.chrome import ChromeDriverManager


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


#### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()


#### JPL Space Images Featured Image

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


#### Mars Facts

df = pd.read_html('https://galaxyfacts-mars.com')[0]


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)


df.to_html()


## D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
#### Hemispheres
# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
links = browser.find_by_css('a.product-item img')
 
for img in range(len(links)):
    
    # Create an empty dict.to store imgs:
    hemisphere = {}
        
    # Find the img and click through to next page/img:
    browser.find_by_css('a.product-item img')[img].click()
        
    sample_elem = browser.links.find_by_text('Sample').first
        
    hemisphere['img_url']=sample_elem['href']
    
    # Get the title:
    
    hemisphere['title'] = browser.find_by_css('h2.title').text
    
    
    # append list with dictionary:
    
    hemisphere_image_urls.append(hemisphere)
    
    # we need to navigate back to the start page:

    browser.back()
    
# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# 5. Quit the browser
browser.quit()

