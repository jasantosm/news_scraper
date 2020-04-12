#news_page_objects.py
#Programmer: Julián Santos
#Email: ingjuliansantos@gmail.com

import bs4
import requests

from common import config


#These Classes implement the abstraction of a news site

#father NewsPage abstration
class NewsPage:

    def __init__(self, news_site_uid, url):
        self._config = config()['news_site'][news_site_uid] # stores the configuration of the news site to scrap
        self._queries = self._config['queries'] #stores the queries to the site
        self._html = None #stores the html scraped from the page
        self._url = url #stores the page url

        self._visit(url)

    def _select(self, query_string):
        return self._html.select(query_string)

    def _visit(self, url):
        response = requests.get(url)

        response.raise_for_status()

        self._html = bs4.BeautifulSoup(response.text, 'html.parser')

#Home Page abstraction, hierarchy from NewPage
class HomePage(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['homepage_articles_links']):
            if link and link.has_attr('href'):
                link_list.append(link)

        return set(link['href'] for link in link_list)
#Article Page abstraction, hierarchy from NewPage
class ArticlePage(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    @property
    def body(self):
        result = self._select(self._queries['article_body'])

        return result[0].text if len(result) else ''

    @property
    def title(self):
        result = self._select(self._queries['article_title'])

        return result[0].text if len(result) else ''

    @property
    def url(self):
        return self._url
