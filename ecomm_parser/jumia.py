from bs4 import BeautifulSoup as soup
import requests

def get_data(requests,url, soup):
    """ queries the site, basic processing and returns the result_set we need"""
    page_raw = requests.get(url)
    html_file = page_raw.text
    raw_data = soup(html_file, "lxml")
    result_set = raw_data.find_all(True, {'class':['sku -gallery', '-has-offers']}) 
    result = result_set[0]
    return result

def parse_data(result):
    #getting important stuffs needed
    _ = result.find(class_='title')
    brand = _.find(class_='brand').text
    title = _.find(class_='name').text
    link = result.a['href']
    img = result.img['data-src']
    #currency = result.find(class_="price").span['data-currency-iso']
    old_price = result.find(True, {'class': '-old'}).text
    price = result.find(class_="price").text
    discount = result.find(class_="sale-flag-percent").text

    #printing results
    print(brand)
    print(title)
    print(link)
    print(old_price)
    print(price)
    print(discount)

def run():
    result = get_data(requests,'https://www.jumia.com.ng/keyboards-mice-accessories/',soup)
    parse_data(result)

if __name__ == '__main__':
    run()