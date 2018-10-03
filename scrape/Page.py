import json
import logging
import os

from requests import get

from scrape._page import _league_table, _result_matrix, _top_scorers


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
        

        self.logger.info('Getting standings for season..')
        leagueTable = (_league_table._LeagueTable(response.text)).get_league_table()

        if leagueTable is not None:
            self.logger.info('Standings fetched successfully.')
        else:
            self.logger.info(f'Failed to fetch standings for this {self.url}.')

        
        self.logger.info('Getting results for season..')
        results = (_result_matrix._ResultMatrix(response.text)).get_result_matrix()

        if results is not None:
            self.logger.info('Results fetched successfully.')
        else:
            self.logger.info(f'Failed to fetch results for this {self.url}.')

        
        self.logger.info('Getting top scorers for season..')
        topScorers = (_top_scorers._TopScorers(response.text, self.url, self.seasons, self.leagueCode)).get_top_scorers()

        if topScorers is not None:
            self.logger.info('Top scorers fetched successfully.')
        else:
            self.logger.info(f'Failed to fetch top scorers for this {self.url}.')


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
            dumpPath = f'.\\dump\\json\\{self.leagueCode}'
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






        
        




        













