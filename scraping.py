
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = hemisphere_image(browser)
        # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres_dict": hemisphere_image_urls
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
# Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')
    # add try/except for error handling
    try: 
        slide_elem = news_soup.select_one('div.list_text')

        slide_elem.find('div', class_='content_title')


# Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

# Use the parent element to find the first `a` tag and save it as `article teaser`
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    return news_title, news_p

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
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

def mars_facts():
    try:
# Use read_html to scrape facts into a table dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
# Convert to html with pandas
    return df.to_html(classes="table table-striped")

def hemisphere_image(browser):

    #Visit the browser
    hemi_imgs_url = 'https://marshemispheres.com/'
    browser.visit(hemi_imgs_url)
    #Create a list to hold the images and titles.
    hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

    browser.find_by_tag('h3').click()
    for item in range(4):
        hemispheres={}
        browser.find_by_tag('h3')[item].click()
        hemi=browser.find_by_text('Sample').first
        image_rel_url=hemi['href']
        hemispheres['image_url']=image_rel_url
        hemispheres['image_title']=browser.find_by_tag('h2').text
        if hemispheres not in hemisphere_image_urls:
            hemisphere_image_urls.append(hemispheres)
        browser.back()

        return hemisphere_image_urls
    
if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())





