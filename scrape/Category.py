import json
import logging

from bs4 import BeautifulSoup
from requests import get



class Category:
    '''
    Scrape season names across leagues from.. 

    Premier League:
    https://en.wikipedia.org/wiki/Category:Premier_League_seasons

    La Liga:
    https://en.wikipedia.org/wiki/Category:La_Liga_seasons

    Serie A:
    https://en.wikipedia.org/wiki/Category:Serie_A_seasons

    Bundesliga:
    https://en.wikipedia.org/wiki/Category:Bundesliga_seasons
    '''


    def __init__(self):

        logging.basicConfig(level=logging.INFO)
        '''
        logging.basicConfig(filename=f'./scrape/{__name__}.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)
       '''
        self.logger = logging.getLogger(__name__)
        self.logger.info('-----------------------------------------------------------------------------------')
        self.logger.info(f"Initializing {__name__}.")

        self.leagueCategoryLinks = {
            'pl':'https://en.wikipedia.org/wiki/Category:Premier_League_seasons',
            'll':'https://en.wikipedia.org/wiki/Category:La_Liga_seasons',
            'sa':'https://en.wikipedia.org/wiki/Category:Serie_A_seasons',
            'bl':'https://en.wikipedia.org/wiki/Category:Bundesliga_seasons'
        }
        self.logger.debug(f'leagueCategoryLinks:{self.leagueCategoryLinks}')



    def get_league_seasons(self, leagueCode:str) -> dict:
        """
        Does requests.get() to league category page  
        
        Arguments:
            leagueCode -- 'pl'||'ll'||'sa'||'bl' 
        
        Returns:
            dict -- {
                'season-name1':'url-to-season1-page',
                'season-name2:'url-to-season2-page',
                .
                .
                'season-nameN':'url-to-season3-page'
            }
        """

        self.logger.debug(f'Page:{self.leagueCategoryLinks[leagueCode]}.')
        self.logger.info(f'Doing get on {self.leagueCategoryLinks[leagueCode]}.')

        response = get(self.leagueCategoryLinks[leagueCode])
        self.logger.info(f'Request made with status code: {response.status_code}.')
        #self.logger.debug(response.text)

        
        allSeasonsLinks = self.process_response(response.text)
        self.logger.info('Processing response complete..!')
        return allSeasonsLinks



    def process_response(self, responseText:str) -> dict:
        """Process the source code in response.text and return a dict of season names and their page links
        
        Arguments:
            responseText {str} -- response.text
        
        Returns:
            dict -- {
                'season-name1':'url-to-season1-page',
                'season-name2:'url-to-season2-page',
                .
                .
                'season-nameN':'url-to-season3-page'
            }
        """

        self.logger.info('Creating BeautifulSoup object for response.text.')
        content = BeautifulSoup(responseText, features='lxml')
        #self.logger.debug(f'Content:{content}')

        div = None
        divText = None

        for div in content.findAll('div', attrs={'class':'mw-category-group'}):
            div = div
            divText = div.text
        
        #self.logger.debug(f'div:{div}')
        #elf.logger.debug(f'divText:{divText}')

        leagueSeasonsName = divText.split('\n')

        #eliminate '0-9' which is first element in list 
        leagueSeasonsName = leagueSeasonsName[1:len(leagueSeasonsName)]
        self.logger.debug(f'len(leagueSeasonsName) =  {len(leagueSeasonsName)}')

        #div has links for actual wikipedia pages of different seasons enclosed in '<a>' tags
        #get those links and store them in list for further processing
        #self.logger.debug(div)

        leagueSeasonsUrls = []
        #don't need to parse divs again hmm?
        #parse the str into 'BeautifulSoup' object
        #div = BeautifulSoup(div, features='lxml')
        #find all 'href's in div 
        for a in div.find_all('a', href=True):
            leagueSeasonsUrls.append(f"https://en.wikipedia.org{a['href']}")
        
        #self.logger.debug(f'leagueSeasonsUrls: {leagueSeasonsUrls}')

        '''
        #it is of paramount importance to have list of leagueSeasons and urls of same list 
        #(sort of verified it using len() but still writing this jic I forget)
        #if they are not of same length and zipped might result in truncation of larger list and in 
        #worst case wrong page urls associated with wrong leagueSeason
        '''

        leagueSeasons = dict(zip(leagueSeasonsName, leagueSeasonsUrls))
        self.logger.debug(f'Final dict:{leagueSeasons}')

        return leagueSeasons
