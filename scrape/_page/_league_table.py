import logging
import re

from bs4 import BeautifulSoup



class _LeagueTable:
    '''Scrapes standings of a league a from given url
    '''


    def __init__(self, responseText:str):

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

        self.responseText = responseText
        
        self.tableAttrsList = [
            {'class':'wikitable', 'style':'text-align:center;'},
            {'class':'wikitable sortable', 'style':'text-align:center;'},
            {'class':'wikitable', 'style':'text-align: center'}
        ]
        
        self.logger.debug(f'tableAttrsList = {self.tableAttrsList}')

        self.logger.info(f'Initializing {__name__} complete..!')



    def get_league_table(self) -> list:
        '''League table converted to list of list, where each list is one row of table.
        
        Arguments:
            responseText {str} -- response.text 
        
        Returns:
            list -- [[row1], [row2], [row3], ...,[rowN]]
        '''

        self.logger.info('Processing response..')
        processedResponse = self.process_response()

        if processedResponse is None:
            self.logger.debug(f'tableAttrs failed here.')
            return
        else:
            self.logger.info('Response Processed..!')
            return processedResponse



    def process_response(self) -> list:
        '''League table converted to list of list, where each list is one row of table.
        
        Arguments:
            responseText {str} -- response.text
        
        Returns:
            list -- [[row1], [row2], [row3], ...,[rowN]]
        '''


        self.logger.info('Creating BeautifulSoup object for response.text.')
        selectedSeasonPage = BeautifulSoup(self.responseText, features='lxml')
        leagueTableRaw = None


        #idk how i thought this up lol, original one I wrote used nested try/except blocks to do this
        for attrs in self.tableAttrsList:
            self.logger.info(f"Trying with 'attrs={attrs}")
            leagueTableRaw = selectedSeasonPage.find('table', attrs=attrs)
    
            if leagueTableRaw == None:
                self.logger.info('This attrs did not work. Trying other attrs.')
                #no need to pass 
            else:
                self.logger.info('This attrs worked! Table extracted successfully!')
                self.logger.debug(f'attrs = {attrs}')
                break
        
        #some extra error checking
        if leagueTableRaw == None:
            self.logger.info('Tried all available attrs. Table extraction still failed.')
            return
        
        
        self.logger.info('Processing table..')

        leagueTableRows = leagueTableRaw.find_all('tr')
        self.logger.debug(f'len(leagueTableRows):{len(leagueTableRows)}')

        #first row in table is headers
        #everyone hates \n so remove them by any means possible
        #also dont need qualification/relegation column(last column), drop it 
        leagueTableHeaders = [re.sub('[\\(\\[].*?[\\)\\]]', '', header.strip()) for header in leagueTableRows[0].text.split('\n\n')]

        #this is weird bug that was found in bundesliga seasons 2008+ correcting it now
        if '\n' in leagueTableHeaders[-1]:
            print(True)
            leagueTableHeaders = leagueTableHeaders + leagueTableHeaders[-1].split('\n')
            leagueTableHeaders.pop(-3)

        leagueTableHeaders = leagueTableHeaders[:-1]
        self.logger.debug(f'leagueTableHeaders: {leagueTableHeaders}')

        leagueTable = []
        leagueTable.append(leagueTableHeaders)

        for row in range(1,len(leagueTableRows)):

            #re.sub('[\\(\\[].*?[\\)\\]]', '', header.strip())
            leagueTableRow = [re.sub('[\\(\\[].*?[\\)\\]]', '', text.replace(u'\xa0', u' ').strip()).strip() for text in leagueTableRows[row].text.split('\n\n')]

            if len(leagueTableRow) == len(leagueTableHeaders):
                leagueTable.append(leagueTableRow)
            else:
                #one extra column spotted skip it..
                leagueTable.append(leagueTableRow[:-1])

        
        self.logger.debug(f'leagueTable: {leagueTable}')
        return leagueTable
