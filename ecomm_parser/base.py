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
    
   
    def search(self, query=None, page=1):
        """
        @param page: `type` `int` if specified parses the page num you want 
        Returns results in a `dict` with values `brand`, `item name`, `price`, `link`
        `discount`, and `old price` 
        """
        query = query.rstrip('/') + '/?page={}'.format(page)
        processed_query = self.replace_spaces(query)
        results = None
        try:
            soup = self.get_soup(processed_query)
            results = self.parse_soup(soup)
        except Exception as e:
            print("request cannot be processed. Search returned: {}".format(e))
        search_results = self.parse_results(results)
        return self.display_result_related(search_results)
 
    
    #TODO find a beta way to reimplement this 
    def search_get_discount(self, query, page=1, discount=None,start_num=None, end_num=None):

        """
        works exactly like <search> method but it opens the browser with the links of the 
        discount value or more than the discount value selected.
        @param `start_num` and `end_num` if specified tells where crawler which pages to start
        crawling and where to stop
        `Note: if you don't specify `page` please do so to specify other `keyword arguments`
        example:` ``j.search_get_discount(query,discount=value ,start_num=value, end_num=value)``
        """
        if start_num and end_num is not None:
            
            while(start_num < end_num):
                query = query.rstrip('/') + '/?page={}'.format(start_num)
                
                # show current page the crawler is processing
                print('{}. Processing Page {}.{}'.format('.'*25, start_num ,'.'*25))
                results = self.parse_results(self.parse_soup(self.get_soup(self.replace_spaces(query))))
                self.discount_iter(results, discount=discount)
                start_num = start_num + 1
                            
            else:
                query = query.rstrip('/') + '/?page={}'.format(end_num)
                
                # show last page the crawler is processing
                print('{}. Processing Page {}.{}'.format('.'*25, end_num ,'.'*25))
                results = self.parse_results(self.parse_soup(self.get_soup(self.replace_spaces(query))))
                return self.discount_iter(results, discount=discount)
            
        
        else:
            
            print('{}. Processing Page {}.{}'.format('.'*25, page ,'.'*25))
            query = query.rstrip('/') + '/?page={}'.format(page)
            results = self.parse_results(self.parse_soup(self.get_soup(self.replace_spaces(query))))
            return self.discount_iter(results, discount=discount)
            
    
    @staticmethod
    def discount_iter(results, discount=None):
        result_list = list(zip(*results.values()))    
        for x,y in zip(range(sum(map(len, results.values()))),result_list):
            try:
                if 'no discount' in y[4]:
                    continue
                value = BaseScrapper.discount_stripper(y[4])
                if value <= discount:
                    webbrowser.open(y[3])
                else:
                    print(" **'item {}'** does not meet the discount value you provided".format(y[1]))
            except Exception:
                continue
        

        
        