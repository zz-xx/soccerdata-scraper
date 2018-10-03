import json
import logging
import os

from process import Clean
from process._Plot import _BarPlot, _BoxPlot, _PieChart



class Plot:
    '''Interface to control other plotting classes and combine them into reports
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
        self.logger.info(f'Initializing {__name__}.')
        self.logger.info(f'Initializing {__name__} complete..!')



    def plot_single_season_report(self, page:dict, season:str, leagueCode:str, seasons:dict):
        '''Plots report for data of single season
        
        Arguments:
            page {dict} -- scraped data of page
            season {str} -- season name to which page belongs
            leagueCode {str} -- league code for page
            seasons {dict} -- dictionary of page names and their urls
        '''

        #first make directory for league and current season
        


        #set location for storing graphs create folders if they dont already exist
        location = f'.\\dumps\\graphs\\{leagueCode}\\{season}'
        if not os.path.exists(location):
            os.makedirs(location)
        

        #Box plots for GF (Goals For), GA (Goals Against), Pts (Points), W (Wins), L(Losses)
        standingsDf = (Clean.CleanStandings(page)).make_df()
        values = [standingsDf['GF'].tolist(), standingsDf['GA'].tolist(), standingsDf['Pts'].tolist(), standingsDf['W'].tolist(), standingsDf['L'].tolist(), standingsDf['D'].tolist()]
        labels = ['GF', 'GA', 'Pts', 'W', 'L', 'D']
        title = 'Statistics for GF (Goals For), GA (Goals Against), Pts (Points) <br> and W (Wins), L (Losses),D (Draws)'
        _BoxPlot._BoxPlot(title, labels, values, location + '\\BoxPlot.html').make_box_plot(subplot=False)

        
        #make home wins, away wins and draws pie chart
        winsDf = (Clean.CleanResults(page)).make_win_statistics_df()
        (_PieChart._PieChart('Win Statistics', location + '\\WinsPieChart.html')).make_win_type_chart(winsDf)

        #wins and loses by percent according to teams
        (_PieChart._PieChart('Overall Win and Lose percent by teams', location + '\\OverallWinsPie.html')).make_standings_donut_chart(standingsDf)

        #make bar chart for home and away goals by teams
        labels, resultsDfList = (Clean.CleanResults(page)).make_results_df()
        (_BarPlot._BarPlot('Home and Away Goals scored by all teams', location + '\\HomeAwayBar.html')).make_home_away_goals_chart(labels, resultsDfList, standingsDf)
        


        


    
        























