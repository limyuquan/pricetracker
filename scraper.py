from bs4 import BeautifulSoup
import requests
from retry import retry
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep

from proxy_tester import reading_proxy, test_proxy_production, get_response

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}

def get_soup_splash(product, site):
    url = f"{site}={get_link(product)}"
    response = requests.get(f"http://localhost:8050/render.html", headers=headers, params={"url" : url, "wait": 2 })
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def get_soup(search, site):
    print(get_link(search, site))
    for proxy in reading_proxy("tested_proxies.csv"):
        print("-------------------------")
        response = get_response(proxy, get_link(search, site))
        if response is not None:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
    return None

def get_link(search, site):
    if site == "https://www.lazada.sg/tag/":
        search = search.strip().lower().replace(" ","-")
        return f"{site}{search}?ajax=true&page=1"
    else:
        return f"{site}{search.strip().lower()}"

def get_keywords(string):
    return string.strip().lower()


@retry()
def amazon_scraper(product):
    site = "https://www.amazon.sg/s?k="
    items = get_soup(product, site).find_all("div", class_="a-section a-spacing-base")
    productData = []
    data = {}
    for item in items:
        name = item.find("span", class_= "a-size-base-plus a-color-base a-text-normal").text
        sponsored = item.find("span", class_= "aok-inline-block s-sponsored-label-info-icon")
        if sponsored is None:
            data = {}
            data["name"] = name
            data["price"] = item.find("span", class_= "a-offscreen").text.replace("S$", "")
            directory = item.find("a", class_= "a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal").attrs["href"]
            data["url"] = f"https://www.amazon.sg{directory}"
            prime = item.find("i", class_="a-icon a-icon-prime a-icon-medium")
            if prime is not None:
                international = item.find("span", class_="a-color-base puis-light-weight-text").text
                if international is not None:
                    location = "Prime and International"
                else:
                    location = "Prime and Singapore"
            else:
                location = "Non Prime"
            data["location"] = location
            productData.append(data)
        return productData

    return(print("error: no items found/end of the list of items"))


def shopee_scraper(product):
    # create object for chrome options
    chrome_options = Options()
    site = "https://shopee.sg/search?keyword="
    base_url = get_link(product, site)

    # set chrome driver options to disable any popup's from the website
    # to find local path for chrome profile, open chrome browser
    # and in the address bar type, "chrome://version"
    chrome_options.add_argument('disable-notifications')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument('user-data-dir=C:\\Users\\darkk\\AppData\\Local\\Google\\Chrome\\User Data\\Default')

    # To disable the message, "Chrome is being controlled by automated test software"
    chrome_options.add_argument('disable-infobars')
    # Pass the argument 1 to allow and 2 to block
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
        })
    # invoke the webdriver
    browser = webdriver.Chrome(executable_path = r'C:\Yu Quan\web_scraper\chromedriver.exe',
                            options = chrome_options)
    browser.get(base_url)
    delay = 5 #secods

    while True:
        try:
            WebDriverWait(browser, delay)
            print ("Page is ready")
            sleep(5)
            html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            soup = BeautifulSoup(html, "html.parser")
            items = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
            i=0
            productData = []
            count = 5

            for item in items:
                data = {}
                if i <= count:
                    ad = item.find('div', class_='Sh+UIZ')
                    name = item.find('div', class_='ie3A+n bM+7UW Cve6sh').text
                    if ad is None and get_keywords(product) in name.lower():
                        data["name"] = item.find('div', class_='ie3A+n bM+7UW Cve6sh').text
                        data["price"] = item.find('span', class_='ZEgDH9').text
                        data["location"] = item.find('div', class_ = 'zGGwiV').text
                        directory = item.find("a").attrs["href"]
                        data["url"] = f"https://shopee.sg{directory}"
                        productData.append(data)
                        i+= 1

            return print(productData)
        except:
            return print("error at end of loop")

def lazada_scraper(product):
    site = "https://www.lazada.sg/tag/"
    url = get_link(product, site)
    print(url)
    for proxy in reading_proxy("tested_proxies.csv"):
        response = get_response(proxy, url)
        print(response)
        if response is not None:
            try:
                response_json = response.json()
                print(response_json)
                break
            except:
                print("no json")

    #         response = response.json()
    #         break
    if response_json is None:
        return print("error in proxy")

    items = response_json["mods"]["listItems"]
    i=0
    productData = []
    count = 5


    for item in items:

        if i < count:
            data = get_data(item["name"],item["priceShow"], item["itemUrl"].lstrip("/"),item["location"])
            productData.append(data)
            i+= 1

    print(productData)
    return productData


    # site = "https://www.lazada.sg/tag/"
    # items = get_soup(product, site).find_all("div", class_="Bm3ON")

def get_data(name, price, link, location):
    data = {}
    data["name"] = name
    data["price"] = price
    data["location"] = location
    data["url"] = link
    return data


if __name__ == "__main__":
    lazada_scraper("airpods pro")