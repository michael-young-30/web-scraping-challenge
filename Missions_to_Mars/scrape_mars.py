
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    executable_path = { "executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    data ={
        "news_title":news_title,
        "news_paragraph":news_paragraph,
        "feature_image":feature_image(browser),
        "facts":mars_facts(),
        "hemispheres":hemispheres(browser)
    }

    browser.quit()
    return data
def mars_news(browser):
    url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html=browser.html
    new_soup=bs(html, 'html.parser')
    try:
        news_paragraph=new_soup.find_all("div",class_="rollover_description_inner")[0].text.strip()
        news_title=new_soup.find_all('div', class_="content_title")[0].text.strip()
    except:
        return None, None
    
    return news_title, news_paragraph

def feature_image(browser):
    url_1='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url_1)
    html=browser.html
    new_soup=bs(html, 'html.parser')
    try:
        full_image_element=new_soup.find("a", class_="showimg fancybox-thumbs")
    except:
        return None
    image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{full_image_element["href"]}'

    return image_url
def mars_facts(browser):

    df = pd.read_html("https://space-facts.com/mars/")[0]
    df.columns=["Description", "Mars"]
    df.set_index("Description", inplace=True)

    return df.to_html(classes="table table-striped")


def hemispheres(browser):
    url_3='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_3)

    hemisphere_image_urls=[]
    links = browser.find_by_css("a.product-item h3")

    for i in range(len(links)):
        hemisphere={}
        browser.find_by_css("a.product-item h3")[i].click()
        try:
            sample_elem=browser.links.find_by_text('Sample').first
            hemisphere['img_url']=sample_elem['href']
            hemisphere['title']=browser.find_by_css("h2.title").text
            hemisphere_image_urls.append(hemisphere)
            browser.back()
        except:
            return None
    return hemisphere_image_urls


