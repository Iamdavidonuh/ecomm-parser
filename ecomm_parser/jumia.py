from bs4 import BeautifulSoup as soup
import requests

page_raw = requests.get('https://www.jumia.com.ng/keyboards-mice-accessories/')
html_file = page_raw.text

raw_data = soup(html_file, "lxml")

result_set = raw_data.find_all(True, {'class':['sku -gallery', '-has-offers']}) 
result = result_set[0]

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