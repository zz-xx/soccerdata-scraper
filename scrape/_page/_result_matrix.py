import logging

from bs4 import BeautifulSoup



class _ResultMatrix:
    '''Scrapes the results of particular season which are stored in form of a matrix
    which can be either color coded or plain.

    Color coding terminology
    #BBF3FF - Home team wins 
    #FFBBBB - Away team wins/Home team loses 
    #FFFFBB - Game is draw
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
            {'style':'font-size: 85%; text-align: center;'},
            {'class':'wikitable plainrowheaders'},
            {'style':'font-size: 100%; text-align: center;'}
        ]
        self.logger.debug(f'tableAttrsList = {self.tableAttrsList}')

        self.tdAttrsList = [
            [{'style':'background-color:#BBF3FF'},
             {'style':'background-color:#FFBBBB'},
             {'style':'background-color:#FFFFBB'}], 
            [{'style':'white-space:nowrap;font-weight: normal;background-color:#BBF3FF;'}, 
             {'style':'white-space:nowrap;font-weight: normal;background-color:#FFBBBB;'},
             {'style':'white-space:nowrap;font-weight: normal;background-color:#FFFFBB;'}]
        ]
        self.logger.debug(f'tableAttrsList = {self.tdAttrsList}')

        self.logger.info(f'Initializing {__name__} complete..!')



    def get_result_matrix(self) -> dict:
        '''Result matrix converted to list of list, where each list 
           is one row of matrix with other info parsed into a dict.
        
        Arguments:
            responseText {str} -- response.text
        
        Returns:
            dict -- {
                'headers': ['h1', 'h2', ...,'hN'], 
                'teams': ['team1', 'team2', ...,'team3'],
                'totalGames': int
                'homeWins': int
                'awayWins': int
                'draws': int
                'results': [[row1], [row2], ...,[rowN]]
            }
        '''


        self.logger.info('Processing response..')
        processedResponse = self.process_response()

        if processedResponse is None:
            self.logger.debug(f'tableAttrs/tdAttrs failed for url.')
            return
        else:
            self.logger.info('Response Processed..!')
            return processedResponse



    def process_response(self) -> list:
        '''Result matrix converted to list of list, where each list 
           is one row of matrix with other info parsed into a dict.
        
        Arguments:
            responseText {str} -- response.text
        
        Returns:
            dict -- {
                'headers': ['h1', 'h2', ...,'hN'], 
                'teams': ['team1', 'team2', ...,'team3'],
                'totalGames': int
                'homeWins': int
                'awayWins': int
                'draws': int
                'results': [[row1], [row2], ...,[rowN]]
            }
        '''
        

        self.logger.info('Creating BeautifulSoup object for response.text.')
        selectedSeasonPage = BeautifulSoup(self.responseText, features='lxml')

        selectedSeasonTable = None
        selectedSeasonTableText = None


        #idk how i thought this up lol, original one I wrote used nested try/except blocks to do this
        for attrs in self.tableAttrsList:
            self.logger.info(f"Trying with 'attrs={attrs}")
            for selectedSeasonTable in selectedSeasonPage.find_all('table', attrs=attrs):
                selectedSeasonTable = selectedSeasonTable
                selectedSeasonTableText = selectedSeasonTable.text
    
            if selectedSeasonTable is None:
                self.logger.info('This attrs did not work. Trying other attrs.')
                #no need to pass 
            else:
                self.logger.info('This attrs worked! Table extracted successfully!')
                self.logger.debug(f'attrs = {attrs}')
                break
        
        #some extra error checking
        if selectedSeasonTable is None:
            self.logger.info('Tried all available attrs. Table extraction still failed.')
            return
        

        #calculate home and away wins by color code if color code exists
        totalGames = None
        homeTeamWins = None
        awayTeamWins = None
        draws = None 

        for attrs in self.tdAttrsList:

            self.logger.info(f"Trying with 'attrs={attrs}..")
            homeTeamWins = [td for td in selectedSeasonTable.find_all('td', attrs=attrs[0])]
            awayTeamWins = [td for td in selectedSeasonTable.find_all('td', attrs=attrs[1])]
            draws = [td for td in selectedSeasonTable.find_all('td', attrs=attrs[2])]

            #can check all 3 vars for 0 but checking one is enough
            if len(homeTeamWins) == 0:
                self.logger.info('This attrs did not work. Trying other attrs.')
                #no need to pass 
            else:
                self.logger.info('This attrs worked! Table extracted successfully!')
                totalGames = len(homeTeamWins) + len(awayTeamWins) + len(draws)
                self.logger.debug(f'attrs = {attrs}')
                self.logger.debug(f'homeTeamWins = {len(homeTeamWins)}')
                self.logger.debug(f'awayTeamWins = {len(awayTeamWins)}')
                self.logger.debug(f'draws = {len(draws)}')
                self.logger.debug(f'totalGames = {totalGames}')
                break
            
        #if it's still none, table is without color codes
        #none indicates need to calculate total games other way 
        if len(homeTeamWins) == 0:
            self.logger.info('No color coding detected in results matrix.')
            '''
            totalGames = None
            homeTeamWins = None
            awayTeamWins = None
            draws = None
            '''
            return
        else:
            homeTeamWins = len(homeTeamWins)
            awayTeamWins = len(awayTeamWins)
            draws = len(draws)
        
        
        self.logger.info('Processing table..')
        #get all rows of table in a list
        selectedSeasonTableRows = selectedSeasonTable.find_all('tr')

        #we need to get headers which are first row in table
        #splitting the first row and getting a list 
        #first 3 elements are useless so they are skipped
        selectedSeasonTableHeaders = selectedSeasonTableRows[0].text.split()[3:len(selectedSeasonTableRows[0].text.split())]
        self.logger.debug(f'selectedSeasonTableHeaders = {selectedSeasonTableHeaders}')

        selectedSeasonTableText = []
        selectedSeasonTeamNames = []

        #need to start from 2nd row since first row is header which we already have
        for row in range(1, len(selectedSeasonTableRows)):
            
            currentRow = selectedSeasonTableRows[row]

            #get list of all cells in row
            currentRowCells = currentRow.find_all('td')
            #print(currentRowCells)

            #u'\xa0' is unicode for space so replaced it with that
            #stripped all '\n' from all string elements in list
            #if condition is to ensure no empty character goes in list, it's just replaced with '-'
            #would make working with pandas easier later
            currentRowValues = [element.text.replace(u'\xa0', u' ').strip() if element.text.replace(u'\xa0', u' ').strip() else '-' for element in currentRowCells]

            #this is for flavor 1 type of tables
            #otherwise team names from flavor 1 table won't show
            #doing this in end bc currentRowValues is created through comprehension
            currentRowTeamName = currentRow.find_all('th')
            #print(currentRowTeamName)
            if currentRowTeamName:
                currentRowValues.insert(0,currentRowTeamName[0].text.strip())
                selectedSeasonTeamNames.append(currentRowTeamName[0].text.strip())
            else:
                selectedSeasonTeamNames.append(currentRowValues[0])
            
            selectedSeasonTableText.append(currentRowValues)
 
        self.logger.debug(f'selectedSeasonTableText = {selectedSeasonTableText}')
        self.logger.debug(f'selectedSeasonTeamNames = {selectedSeasonTeamNames}')

        self.logger.info('Table processed..!')

        self.logger.info('Parsing all info into a dict.')

        processedResponse = {
            'headers': selectedSeasonTableHeaders,
            'teams': selectedSeasonTeamNames,
            'totalGames': totalGames,
            'homeTeamWins': homeTeamWins,
            'awayTeamWins': awayTeamWins,
            'draws': draws,
            'results': selectedSeasonTableText
        }
        self.logger.debug(f'processedResponse = {processedResponse}')

        return processedResponse


            



        



        

        

        





        













    



    






