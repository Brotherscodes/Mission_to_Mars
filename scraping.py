# Import the needed dependencies:
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# Initialize the browser, Create a data dictionary, End the WebDriver and return the scraped data:
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

####################################################################################################

# Create a Function to get the title and paragraph from mars site:
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

####################################################################################################

# Function to scrape our featured image:
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_button = browser.find_by_tag('button')[1]
    full_image_button.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add a try and except for error handling:
    try:
        # Find the relative image url
        img_rel_url = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:

        return None


    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_rel_url}'

    return img_url

#######################################################################################################

### Using a function, Scrape full table with Pandas into a DataFrame to display:

def mars_facts():

    # Add a try and except for error handling:
    try:

        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe:
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format and add Bootstrap:
    return df.to_html(classes="table table-striped")

###########################################################################################################

# hemisphere app function:

def hemispheres(browser):

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

    return hemisphere_image_urls

#######################################################################################################

if __name__ == "__main__":
    
    
    # If running as script, print scraped data
    print(scrape_all())
