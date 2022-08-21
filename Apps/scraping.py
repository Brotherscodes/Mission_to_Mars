# Import needed dependencies:
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

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
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

#####################################################################################################

# Define functions for mars_news to allow it to function with Flask:

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Set up the html parser:
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add a try and except for error handling:
    try:

        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None,None

    return news_title, news_p



##################################################################################################

### Featured Images from JPL:

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

#####################################################################################################


# Facts about Planets table scrape:
### Scraping full table with Pandas into a DataFrame:

def mars_facts():

    # Add a try and except for error handling:
    try:

        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)


# Convert dataframe into HTML format and add Bootstrap:
    return df.to_html(classes="table table-striped")


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

