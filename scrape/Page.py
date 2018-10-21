import json
import logging
import os

from requests import get

from scrape._page import _LeagueTable, _ResultMatrix, _TopScorers


class Page:
    '''Scrapes all the data on page url and returns it in 'structured' form
    '''


    def __init__(self, season:str, leagueCode:str, seasons:dict):

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
        self.logger.info(f'Initializing {__name__}.')
        
        self.leagueCode = leagueCode
        self.season = season
        self.seasons = seasons
        self.url = self.seasons[self.season]

        self.logger.debug(f'leagueCode : {self.leagueCode}')
        self.logger.debug(f'url : {self.url}')

        self.logger.info(f'Initializing {__name__} complete..!')



    def get_data(self,  dump=False) -> dict:
        '''Returns all of page data in dictionary and optionally dumps it into db or json file
        
        Returns:
            dict -- {'standings' : [],
                     'results' : {},
                     'topScorers' : []
            }
        '''

        self.logger.info(f'Doing get on {self.url}.')
        response = get(self.url)
        self.logger.info(f'Request made with status code: {response.status_code}.')


        #this is questionable way to do this but try and except is acceptable way
        #to do flow control in python
        leagueTable = None
        results = None
        topScorers = None
        
        try:
            leagueTableScraper = _LeagueTable._LeagueTable(response.text) 
            self.logger.info('Getting standings for season..')
            leagueTable = leagueTableScraper.get_league_table()
            self.logger.info('Standings fetched successfully.')
        except:
            self.logger.exception(f'Failed to fetch standings for this {self.url}.')

        try:
            resultsScraper =  _ResultMatrix._ResultMatrix(response.text) 
            self.logger.info('Getting results for season..')
            results = resultsScraper.get_result_matrix()
            self.logger.info('Results fetched successfully.')
        except:
            self.logger.exception(f'Failed to fetch results for this {self.url}.')

        try:
            topScorersScraper = _TopScorers._TopScorers(response.text, self.url, self.seasons, self.leagueCode)
            self.logger.info('Getting top scorers for season..')
            topScorers = topScorersScraper.get_top_scorers()
            self.logger.info('Top Scorers fetched successfully.')
        except:
            self.logger.exception(f'Failed to fetch top scorers for this {self.url}.')


        self.logger.info('Parsing all page data together...')
        pageData = {
            'Standings' : leagueTable,
            'Results' :  results,
            'Top Scorers' : topScorers
        }
        self.logger.debug(f'pageData = {pageData}')
        self.logger.info('Parsed page data successfully.')

       
        if dump == True:

            #dumping scrape data into a JSON file 
            #maybe switch to mongo later which seems more suitable
            dumpPath = f'.\\dumps\\json\\{self.leagueCode}'
            if not os.path.exists(dumpPath):
                os.makedirs(dumpPath)

            dumpDict = {
                'league': self.leagueCode,
                'season': self.season,
                'data' : pageData
            }

            with open(f'{dumpPath}\\{self.season}.json', 'w') as writeJSON:
                json.dump(dumpDict, writeJSON)
        

        return pageData
