# Import Splinter and BeautifulSoup dependencies:
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# Set the executable path and initialize the browser:
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Set up the html parser:
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

# Find the title and scrape it:
slide_elem.find('div', class_='content_title')


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


### Featured Images from JPL:

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
img_rel_url


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_rel_url}'
img_url


# Facts about Planets table scrape:

### Scraping full table with Pandas into a DataFrame:

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# Update your app.py to include this new df we made: # We can add by adding this exact output of code to
# our app:
df.to_html()


# Always tell your browser to quit when youre done to close the browser:
browser.quit()





