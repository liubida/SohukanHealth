'''
Created on 2012-6-7

@author: diracfang
'''

import urllib2
import httplib2
import random
from BeautifulSoup import BeautifulSoup
import urlparse
import re

class RandomSpider(object):
    """spider for get some random page url from website
    
    currently available sites:
    ifanr, engadget, 163, sina, sohu
    
    you can specify sites manually using self.specify_sites(site_names)
    """
    
    def __init__(self):
        self._site_mapper = {
#                             'ifanr': 'http://www.ifanr.com/',
#                             'engadget': 'http://cn.engadget.com/',
#                             'sina': 'http://news.sina.com.cn/',
                             'sohu': 'http://news.sohu.com/',
                             }
        self._patterns = {
#                          'www.ifanr.com': '/\d+',
#                          'cn.engadget.com': '/\d+',
#                          'news.sina.com.cn': '/(pl|[cswm])/.+',
                          'news.sohu.com': '/\d+',
                          }
        for i in self._patterns:
            self._patterns[i] = re.compile(self._patterns[i])
        self._available_sites = []
        for i in self._site_mapper:
            self._available_sites.append(i)
        self._enabled_sites = self._available_sites[:]
    
    def _map_site(self, site_name):
        return self._site_mapper[site_name]
    
    def _fetch_url(self, url):
        try:
            page = urllib2.urlopen(url).read()
        except:
            page = None
        
        return page
            
    def _get_index_page(self):
        url = None
        page = None
        for i in range(10):
            try:
                url = self._map_site(random.choice(self._enabled_sites))
                page = self._fetch_url(url)
            except:
                pass
            else:
                break
        
        return url, page
    
    def _is_required_pattern(self, index_url, link):
        is_required_pattern = False
        if self._is_same_domain(index_url, link):
            domain = urlparse.urlparse(index_url)[1]
            pattern = self._patterns.get(domain, None)
            if pattern:
                path = urlparse.urlparse(link)[2]
#                print path,
                if pattern.match(path):
                    is_required_pattern = True
#                    print True
#                else:
#                    print False
            else:
                is_required_pattern = True
        
        return is_required_pattern
    
    def _get_links(self, index_url, page):
        soup = BeautifulSoup(page)
        links = []
        for tag in soup.findAll('a'):
            link = tag.get('href', None)
            link = urlparse.urljoin(index_url, link)
            link = httplib2.iri2uri(link)
            if link and self._is_required_pattern(index_url, link):
                links.append(link)
        links_set = set(links)
        links = list(links_set)
                
        return links
    
    def _is_same_domain(self, link1, link2):
        domain1 = urlparse.urlparse(link1)[1]
        domain2 = urlparse.urlparse(link2)[1]
        if domain1 == domain2:
            return True
        else:
            return False
        
    def _is_link_valid(self, possible_link):
        page = self._fetch_url(possible_link)
        if page:
            return True
        else:
            return False
        
    def specify_sites(self, site_names):
        """manually specify site, when you have to"""
        self._enabled_sites = []
        for site_name in site_names:
            if site_name in self._available_sites:
                self._enabled_sites.append(site_name)
        
        return None
    
    def get_valid_url(self):
        valid_link = None
        for i in range(10):
            index_url, page = self._get_index_page()
            if index_url and page:
                break
        if index_url and page:
            links = self._get_links(index_url, page)
        else:
            links = []
        if links:
            for i in range(10):
                possible_link = random.choice(links)
                if self._is_link_valid(possible_link):
                    valid_link = possible_link
                    break
        
        return valid_link


if __name__ == '__main__':
    s = RandomSpider()
#    s.specify_sites(['ifanr'])
    for i in range(10):
        url = s.get_valid_url()
        if url:
            print 'chosen: %s' % url
        else:
            print 'not found'
        
