import logging
import re

from bs4 import BeautifulSoup



class _TopScorers:
    '''Get top scorers of the season
    '''


    def __init__(self, responseText:str, url:str, seasons:dict, leagueCode:str):

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

        self.page = BeautifulSoup(responseText, features='lxml')
        self.seasons = seasons
        self.leagueCode = leagueCode
        self.url = url

        self.tableIds = [{"id": "Top_scorers"},
                         {"id": "Pichichi_Trophy"},
                         {"id": "Top_goalscorers"},
                         {"id": "Top_goal_scorers"},
                         {"id": "Leading_scorers"},
                         {"id": "Goals"},
                         {"id": "Pichichi_Trophy_and_La_liga_top_scorers"}
        ]
        self.logger.debug(f'tableIds : {self.tableIds}')
        
        self.logger.info(f'Initializing {__name__} complete..!')
        


    def get_top_scorers(self) -> list:
        '''Returns top scorers of a season
        
        Returns:
            list -- [{1},{2},...,{n}]
        '''
        

        #only bl and sa contain some top scorers data without table
        if self.leagueCode in ['bl','sa']:
            self.logger.debug(f'{self.leagueCode} selected.')

            #there's really no other way to do this without creating confusions
            #i hate this but at least it works
            topScorers = self.no_table()

            if topScorers is None:
                topScorers = self.get_table()
                
                #if topScorers is still none then something wrong
                if topScorers is None:
                    self.logger.info('Top Scorers table extraction failed.')
                    return
                else:
                    self.logger.info('Top Scorers table extraction successful.')
                    return topScorers
            
            else:
                self.logger.info('Top Scorers extracted. No table was detected.')
                return topScorers


        #it's not bundesliga or serie a so it must contain a table
        else:
            self.logger.info(f'{self.leagueCode} selected.')
            topScorers = self.get_table()

            #if topScorers is still none then something wrong
            if topScorers is None:
                self.logger.info('Top Scorers table extraction failed.')
                return
            else:
                self.logger.info('Top Scorers table extraction successful.')
                return topScorers



    def no_table(self) -> list:
        '''Returns list of dictionary containing top goal scorers of league
        
        Returns:
            list -- [{1},{2},...,{n}]
        '''

        try:
            topScorersList = []

            for id in self.tableIds:

                x = self.page.find("span", id)
                if x is None:
                    continue
                
                scorer = {
                    'goals' : None,
                    'scorers' : []
                }

                '''
                Assuming single entry looks like this
                16 goals
                 Michel Platini France (Juventus)
                '''

                #if page contains no dl it will return none and throw attribute error here
                #we can catch this and return none and determine if table is present in page 
                #dl has goals
                x = x.parent.find_next_sibling('dl')
                scorer['goals'] = int(x.text.split()[0])

                #ul has player name and team name
                x = x.find_next_sibling('ul')
                scorer['scorers'] = [{'player' : element[:element.find('(')].strip(), 'club' : element[element.find('(')+1:element.find(')')]} for element in x.text.split('\n')]
                
                topScorersList.append(scorer)
                
                while True:
                    try:
                        scorer = {
                            'goals' : None,
                            'scorers' : None
                        }

                        x = x.find_next_sibling('dl')
                        scorer['goals'] = int(x.text.split()[0])
                        #print(x.text)
                        
                        x = x.find_next_sibling('ul')
                        scorer['scorers'] = [{'player' : element[:element.find('(')].strip(), 'club' : element[element.find('(')+1:element.find(')')]} for element in x.text.split('\n')]
                        topScorersList.append(scorer)       
                    
                    except AttributeError:
                        break
            
            self.logger.debug(f'topScorersList = {topScorersList}')
            return topScorersList
            
            
        except AttributeError:
            logging.info('Table detected. Trying to extract table..')
            return None



    def get_table(self) -> list:
        '''Returns list of dictionary containing top goal scorers of league
        
        Returns:
            list -- [{1},{2},...,{n}]
        '''
        
        x = None

        for id in self.tableIds:
            try:
                x = self.page.find("span", id).parent.find_next_sibling('table', {'class':'wikitable'})
            except AttributeError:
                continue
        
        #sort of error checking
        if x is None:
            return
            

        topScorers_list = [z.strip() for z in x.text.split('\n')  if z]
        #print(topScorers_list)

        headers = [re.sub('[\\(\\[].*?[\\)\\]]', '', th.text.strip()) for th in x.find_all('tr')[0].find_all('th')]
        self.logger.debug(f'headers = {headers}')

        topScorers_list = topScorers_list[len(headers):]
        #print(topScorers_list)

        z = []
        #first row header so skipping it
        for element in x.find_all('tr')[1:]:
            c = [z.strip() for z in element.text.split('\n')  if z]
            
            #first row after must always be equal to no of headers
            if len(c) != len(headers):
                z[-1].extend(c)
            
            else:
                z.append(c)

        z1 = []
        for val in z:
            u = []
            goals = None
            #assuming first column is rank
            for i in val[1:]:

                if i.isnumeric():
                    goals = int(i)
                    
                else:
                    u.append(i)
            
            u.insert(0, goals)
            z1.append(u)


        z2 = [{'goals' : i.pop(0), 'scorers' : [{'player': k[0], 'club' : k[1]} for k in [i[j:j+2] for j in range(0, len(i), 2)]]} for i in z1]

        self.logger.debug(f'topScorersList = {z2}')
        return z2


                






    






    

