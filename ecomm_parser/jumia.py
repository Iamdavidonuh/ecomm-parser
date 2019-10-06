from bs4 import BeautifulSoup as soup
import requests

def get_data(requests,url, soup):
    """ queries the site, basic processing and returns the result_set we need"""
    page_raw = requests.get(url)
    html_file = page_raw.text
    raw_data = soup(html_file, "lxml")
    result_set = raw_data.find_all(True, {'class':['sku -gallery', '-has-offers']}) 
    result = result_set
    return result

def parse_data(result_set):
    #getting important stuffs needed
    for result in result_set:
        
        _ = result.find(class_='title')
        brand = _.find(class_='brand').text
        title = _.find(class_='name').text
        link = result.a['href']
        img = result.img['data-src']
        #currency = result.find(class_="price").span['data-currency-iso']
        old_price = result.find(True, {'class': '-old'}).text
        price = result.find(class_="price").text
        try:
            discount = result.find(class_="sale-flag-percent").text
        except Exception:
            discount = "No discount available"
        #printing results
        print('brand: ',brand)
        print('title: ',title)
        print('link: ',link)
        print('old_price: ',old_price)
        print('new_price: ',price)
        print('discount: ',discount)
        print('..........................................................')

def run():
    result = get_data(requests,'https://www.jumia.com.ng/keyboards-mice-accessories/',soup)
    parse_data(result)

if __name__ == '__main__':
    run()