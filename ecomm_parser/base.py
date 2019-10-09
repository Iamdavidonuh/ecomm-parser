from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
import requests
from ecomm_parser.additions import headers
import webbrowser

class BaseScrapper(object):
    __metaclass__ = ABCMeta
    

    
    def replace_spaces(self, url_link=None):
        return url_link.replace(" ", '%20')

    @staticmethod
    def get_source(url_link):
        '''
        get the source code of a webpage. 
        '''
        response = requests.get(url_link,headers = headers)
        html = response.text
        return html
    
    
    def get_soup(self, query=None):
        html = self.get_source(query)
        return BeautifulSoup(html, 'lxml')
    
    @abstractmethod
    def parse_soup(self, soup):
        """
            Returns a every element within the `tag` specified
        """
        return NotImplementedError("You must specify the method <parse_soup> in your subclass")
    @abstractmethod
    def parse_body(self, result_set):
        """
            Returns a every element within the tag specified in other to retrieve the `Item name`,
            `Price`, `Discount Value` and `Link to the particular file`
        """
        return NotImplementedError("You must specify this method(<parse_body>) in your subclass")


    def parse_results(self,result_set):
        """
            Goes through every entry in `parse_body`
            :param results: Results of main search to extract individual entries
            :type results: list[`bs4.element.ResultSet`]
            :returns dictionary of item name, links, price, discount 
            :rtype dict
        """
        search_results = dict()
        for result in result_set:
            try:
                #@param temp rtype is a dict
                temp = self.parse_body(result)                
                #get all keys in temp and compare that with that of `search_results` 
                for key in temp.keys():
                    if key not in search_results.keys():
                        search_results[key] = list([temp[key]])
                    else:
                        search_results[key].append(temp[key])
            except Exception:
                pass
        return search_results
    
    @staticmethod
    def discount_stripper(to_strip):
        discount = int(to_strip.replace("%",""))
        return discount
    
    @staticmethod
    def display_result_related(search_results,):
        """
            Displays the titles, links prices, etc associated with an items `together` rather than in `<parse_results>`
            @param `dr_results` new dictionary that holds all related data as `lists` with `keys(range of len <parse_results dict)` 
            :rtype `dict`

        """
        dr_results = dict()
        _temp = list(zip(*search_results.values())) 
        # range of the sum of the iteration of the number of values in search_results dict
        for x,y in zip(range(sum(map(len, search_results.values()))),_temp):
            dr_results[x] = list(y)
            
        return dr_results
    
    @staticmethod
    def open_link_with_discount(search_results,discount):
        """
        Opens the webbrowser when a particular product has or is above a `discount` specified
        """
        pass

    @staticmethod
    def open_link():
        pass

   
    def search(self, query=None):
        """
        Returns results in a `dict` with values `brand`, `item name`, `price`, `link`
        `discount`, and `old price` 
        """
        processed_query = self.replace_spaces(query)
        results = None
        try:
            soup = self.get_soup(processed_query)
            results = self.parse_soup(soup)
        except Exception as e:
            print("request cannot be processed. Search returned: {}".format(e))
        search_results = self.parse_results(results)
        return self.display_result_related(search_results)
    
    def get_search(self,query=None):
        pass
        
    #TODO find a beta way to reimplement this 
    def search_goto_discount(self, query, discount):
        """
        works exactly like <search> method but it opens the browser with the links of the 
        discount value or more than the discount value selected 
        """
        results = self.parse_results(self.parse_soup(self.get_soup(self.replace_spaces(query))))
        #results = self.parse_results(self.parse_soup(self.replace_spaces(query)))
        result_list = list(zip(*results.values()))    
        for x,y in zip(range(sum(map(len, results.values()))),result_list):
            try:
                if 'no discount' in y[4]:
                    continue
                value = self.discount_stripper(y[4])
                if value <= discount:
                    webbrowser.open(y[3])
                else:
                    print("No item meets the discount provided")
            except Exception:
                continue

        
        

