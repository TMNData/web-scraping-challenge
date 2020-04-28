from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Visit nasa new web
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # collecting all list items form list text div
    article_grid = soup.find_all('div', class_='list_text')

    #Creating empty list to store all news title and short description
    news_title=[]
    news_p=[]

    # iterating and appending title and abstract to list
    for article in article_grid:
        title=article.find('div', class_= "content_title").text
        news_title.append(title)
        abstract=article.find('div', class_= "article_teaser_body").text
        news_p.append(abstract)

    # printing first item from list as request is to print latest article information.

    print(news_title[0])
    print('-------------------------------------')
    print(news_p[0])
    web_title =news_title[0]
    web_body=news_p[0]

    # 2) visiting JPL site

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(4)

    #splinter to navigate the site and find the image url

    browser.click_link_by_partial_text('FULL IMAGE')

    # nevigating to full resolution image

    browser.click_link_by_partial_text('more info')

    html=browser.html
    soup=bs(html, 'html.parser')

    #screaping image partial url

    image_url = soup.find('figure', class_="lede").a['href']

    jpl_url= 'https://www.jpl.nasa.gov/'

    # meargre and full url formation

    featured_image_url= str(jpl_url)+str(image_url)
    print(featured_image_url)
    

# 3) screping marse weather
    
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(5)
    html=browser.html
    soup=bs(html, 'html.parser')

    # Find all span tags and save it in spans list
    spans = soup.find_all('span')
    #for every span in the spans list look for the text sol, low and high that indicates it is a tweet about weather
    for span in spans:
        if 'sol' and 'low' and 'high' in span.text.lower():
            mars_weather = span.text
            #print(mars_weather)
            #break the loop if the first weather tweet is found, since we need only the latest tweet
            break
        else: 
            pass
    #print(mars_weather)
        # screping HTML table and saving as html
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_fact=tables[0]
    mars_fact = mars_fact.rename(columns={0:"Desc.", 1:"Value"})
   
    
    html_mars_fact=mars_fact.to_html(header=True,border=5, index=False)

    #html_mars_fact=mars_fact.to_html('output/mars_fact.html',header=True,border=2, index=False)  

    # 4) Astro 
    # 

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(4)
    html=browser.html
    soup=bs(html, 'html.parser')

    #screaping All result for hemishpher

    lists = soup.find_all('div', class_="item")

    hemisphere_image_urls = []

    for l in lists:
        title= l.h3.text
        url = l.find('a')['href']
        
        #creating link to screap high resolution url
        image_link= "https://astrogeology.usgs.gov/"+url 
        #nevigating to high resolution image
        browser.visit(image_link) 
        time.sleep(2)
        html = browser.html 
        soup = bs(html, "html.parser")
        # capturing high resolution image
        fullimage = soup.find('img', class_='wide-image')['src']  
        img_url = "https://astrogeology.usgs.gov" + fullimage
        #creating and appending dictionary to list
        hemisphere_image_urls.append({"title": title, "img_url": img_url})
     
        
     
   
    # Store data in a dictionary
    mars_data = {
        "News_Title": web_title,
        "New_abstract":web_body,
        "featured_image_url":featured_image_url,
        "Mars_Weather":mars_weather,
        "Mars_Fact": html_mars_fact,
        "Mars_Hemisphere": hemisphere_image_urls,
    }

    # Quite the browser after scraping
    browser.quit()

    # Return results
    return mars_data
