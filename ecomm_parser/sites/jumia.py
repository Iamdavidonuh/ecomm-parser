from ecomm_parser.base import BaseScrapper


class Jumia(BaseScrapper):
    
    #url_link = "https://www.jumia.com.ng/keyboards-mice-accessories/"
    url_link = 'https://www.jumia.com.ng/keyboards-mice-accessories/?page=2'
    def parse_soup(self, soup):
        # find all classes with 'sku -gallery', '-has-offers'' => each result
        return soup.find_all(True, {'class':['sku -gallery', '-has-offers']})
    
    def parse_body(self, result_set):
        _ = result_set.find(class_="title")
        title = _.find(class_='name').text
        brand = _.find(class_='brand').text
        link = result_set.a['href']
        price = result_set.find(class_="price").text
        try:
            discount = result_set.find(class_="sale-flag-percent").text
            old_price = result_set.find(True, {'class': '-old'}).text
        except AttributeError:
            pass
            #print("no discount for item")
        search_results = {
            'brand': brand,
            'title': title,
            'price': price,
            'link': link,
            'discount': discount,
            'old_price': old_price
        }
        return search_results
    