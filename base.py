from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
import requests
from additions import headers

class BaseScrapper(object):
    __metaclass__ = ABCMeta
    
    url_link = None
    
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
                        search_results[key] = list(temp[key])
                    else:
                        search_results[key].append(temp[key])
            except Exception:
                pass
        return search_results
    """
    @staticmethod
    def display_items(result_dict):
        for x,y in result_dict:
            print()
    """
    
    def search(self, query=None):
        processed_query = self.replace_spaces(query)
        results = None
        try:
            soup = self.get_soup(processed_query)
            results = self.parse_soup(soup)
        except Exception as e:
            print("request cannot be processed. Search returned: {}".format(e))
        search_results = self.parse_results(results)
        return search_results
    