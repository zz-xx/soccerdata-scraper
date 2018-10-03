import logging
import re

import numpy as np
import pandas as pd



class CleanStandings:
    '''[summary]
    '''


    def __init__(self, page:dict):

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info('-----------------------------------------------------------------------------------')
        self.logger.info(f'Initializing {__name__}.')

        self.standings = page['Standings']
    


    def make_df(self) -> pd.DataFrame:
        '''Convert standings to pandas dataframe
        '''

        standings = self.standings

        #first list is headers of table so pop it
        standingsHeaders = standings.pop(0)
        #not really required but some standings misbehave..
        #specially in Premier League so this is fail safe to ensure correct header names
        #standingsHeaders = ['Pos', 'Team', 'Pld', 'W', 'D' , 'L' , 'GF', 'GA', 'GD', 'Pts']


        #clean up standings table to ensure only 10 values remain in list
        #last 11th value in list  is useless anyway
        #standings = [standing[:10]for standing in standings]
        #pprint.pprint(standings)

        #convert standings to dataframe using above list as headers
        df = pd.DataFrame(standings, columns=standingsHeaders)

        #start row index with 1 so it can also act as position
        #could delete 'Pos' column but keeping it just in case
        df.index = df.index + 1

        #convert numeric strings to int

        #wasted some real time here trying to figure this out
        #'-' won't work due to intricacies of language :/ 
        #u"\u2212" is unicode for dash
        #x = [int('-' + re.sub("\\D", "", i)) if '-' in i else int(re.sub("\\D", "", i)) for i in list(df['GD'])]

        for header in list(df.columns.values):
            
            if 'Team' not in header:
                df[header] = [int('-' + re.sub("\\D", "", i)) if u"\u2212" in i else int(re.sub("\\D", "", i)) for i in list(df[header])]

        self.logger.debug(f'Standings df = {df}')

        return df




class CleanResults:
    '''[summary]
    '''


    def __init__(self, page:dict):

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info('-----------------------------------------------------------------------------------')
        self.logger.info(f'Initializing {__name__}.')

        #for convenience unpacking it here..
        results = page['Results']

        self.headers = results['headers']
        self.teams = results['teams']
        self.results = results['results']
        self.totalGames = results['totalGames']
        self.homeTeamWins = results['homeTeamWins']
        self.awayTeamWins = results['awayTeamWins']
        self.draws = results['draws']

    

    def make_win_statistics_df(self) -> pd.DataFrame:
        '''make wins statistics pandas dataframe
        '''
 
        #idk why this doesn't works tbh
        #wins = [[self.totalGames], [self.homeTeamWins], [self.awayTeamWins], [self.draws]]
        #df = pd.DataFrame(data=wins, columns=['TotalGames', 'HomeWins', 'AwayWins', 'Draws'])
        
        wins = wins = [[self.totalGames], [self.homeTeamWins], [self.awayTeamWins], [self.draws]]
        columns=['Total Games', 'Home Wins', 'Away Wins', 'Draws']
        df = pd.DataFrame(dict(zip(columns, wins)))
        
        return df
    


    def make_results_df(self):
        '''[summary]
        '''

        #lol could have caused major headaches later 
        #copying because actually new list is needed thus preserving original one
        
        headers = self.teams.copy()
        headers.insert(0, 'Goals')

        resultsDfList = []

        for l in self.results:

            #first value in row is team name
            row = l[1:]

            #re.sub('[\\(\\[].*?[\\)\\]]', '', header.strip())  

            x = [(int(re.sub('[\\(\\[].*?[\\)\\]]', '', element[0])), int(re.sub('[\\(\\[].*?[\\)\\]]', '', element[2]))) if len(element) == 3 else (np.nan, np.nan) for element in row]
        
            #zip returns iterable
            for_ = list(list(zip(*x))[0])
            against = list(list(zip(*x))[1])

            for_.insert(0, 'GF')
            against.insert(0, 'GA')

            #print(headers)
            #print(for_)
            #print(against)

            df = pd.DataFrame([for_, against], columns=headers)
            #print(df)

            df.set_index('Goals', inplace=True)
            #print(df)
            
            #print(df.loc['A'])

            resultsDfList.append(df)
        
        #dont really need to return teams but doing it anyway
        return self.teams, resultsDfList
  