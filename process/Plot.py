import json
import logging
import os

from process import _Clean as Clean
from process import _Report as Report
from process._Plot import _BarPlot, _BoxPlot, _DistPlot, _HeatMap, _LinePlot, _PieChart, _BubbleChart




class Plot:
    '''Interface to clean data, control other plotting classes and combine them into reports
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



    def plot_single_season_report(self, page:dict, season:str, leagueCode:str, seasons:dict, dump=False):
        '''Plots report for data of single season
        
        Arguments:
            page {dict} -- scraped data of page
            season {str} -- season name to which page belongs
            leagueCode {str} -- league code for page
            seasons {dict} -- dictionary of page names and their urls
        '''
        
        #initialize dataframe variables
        standingsDf = None
        resultsDfLabels, resultsDfList = None, None

        #clean the scraped data and get it into pandas dataframes for further analysis
        if page['Standings'] is not None:
            try:
                cleanStandings = Clean.CleanStandings(page) 
                standingsDf = cleanStandings.make_df()
            except Exception:
                self.logger.info("Failed to convert Standings into DataFrame.")
                self.logger.exception("Failed to convert Standings into DataFrame.")

        if page['Results'] is not None:
            try:
                cleanResults = Clean.CleanResults(page)
                resultsDfLabels, resultsDfList = cleanResults.make_results_df()
            except Exception:
                self.logger.info("Failed to convert Results into DataFrame.")
                self.logger.exception("Failed to convert Results into DataFrame.")

        
        #first make directory for league and current season
        #set save path for storing graphs create folders if they dont already exist
        savePath = f'.\\dumps\\graphs\\{leagueCode}\\{season}'
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        
        
        #initialize graphs variables
        standingsBoxPlot = None
        homeAwayWinsPie = None
        winLosePercentTeamsPie = None
        homeAwayGoalsBar = None
        goalsDifferenceHisto = None
        goalsNormalDistPlot = None
        topScorersGoalsLinePlot = None
        bestDefenseBubble = None
        bestOffenseBubble = None
        homeAwayPointsLinePlotsByTeams = None


        #make line plot for goals scored by top scorers
        if page['Top Scorers'] is not None:
            try:
                linePlotter = _LinePlot._LinePlot()
                topScorersGoalsLinePlot = linePlotter.make_top_scorers_goals_plot(page, savePath + '\\TopScorersLinePlot.html', dump=dump)
            except Exception:
                self.logger.info("Failed to draw Top Scorers Goals Line Plot.")
                self.logger.exception("Failed to draw Top Scorers Goals Line Plot.")


        if standingsDf is not None:

            #Box plots for GF (Goals For), GA (Goals Against), Pts (Points), W (Wins), L(Losses)
            try:
                values = [standingsDf['GF'].tolist(), standingsDf['GA'].tolist(), standingsDf['Pts'].tolist(), standingsDf['W'].tolist(), standingsDf['L'].tolist(), standingsDf['D'].tolist()]
                text = standingsDf['Team']
                labels = ['GF', 'GA', 'Pts', 'W', 'L', 'D']
                title = 'Statistics for #GF (Goals For), #GA (Goals Against), #Pts (Points) <br> and #W (Wins), #L (Losses), #D (Draws)'
                boxPlotter = _BoxPlot._BoxPlot(title, labels, values, text, savePath + '\\BoxPlot.html')
                standingsBoxPlot = boxPlotter.make_box_plot(dump=dump)
            except Exception:
                self.logger.info("Failed to plot Standings Box Plot.")
                self.logger.exception("Failed to plot Standings Box Plot.")

            #wins and loses by percent according to teams
            try:
                title = 'Overall #Win and #Lose percent by teams'
                pieChartPlotter = _PieChart._PieChart(title, savePath + '\\OverallWinsPie.html')
                winLosePercentTeamsPie = pieChartPlotter.make_standings_donut_chart(standingsDf, dump=dump)
            except Exception:
                self.logger.info("Failed to plot Overall Wins and Loses percentage Pie chart.")
                self.logger.exception("Failed to plot Overall Wins and Loses percentage Pie chart.")
       
            #make histogram for goal difference according to standings
            try:
                title = '#Goals Difference (GD) based on Final Standings'
                barPlotter = _BarPlot._BarPlot(title, savePath + '\\GoalDifferenceBar.html' )
                goalsDifferenceHisto = barPlotter.make_gd_chart(standingsDf, dump=dump)
            except Exception:
                self.logger.info("Failed to plot Goals Difference Histogram.")
                self.logger.exception("Failed to plot Goals Difference Histogram.")
            
            #make distplot for GA, GF and GD
            try:
                title = 'Distplot with Normal Distribution for <br> #GF (Goals For), #GA (Goals Against) <br> and #Goals Difference (GD)'
                distPlotter = _DistPlot._DistPlot(title, savePath + '\\GoalsDistPlot.html')
                goalsNormalDistPlot = distPlotter.make_normal_goal_distribution(standingsDf, dump=dump)
            except Exception:
                self.logger.info("Failed to plot Distplot for goals with normal distribution.")
                self.logger.exception("Failed to plot Distplot for goals with normal distribution.")
            
            #make bubble chart for teams with best offense and defense
            try:
                bubbleChartPlotter = _BubbleChart._BubbleChart(season, standingsDf)
                bestDefenseBubble = bubbleChartPlotter.best_defensive_teams(savePath + '\\BestDefenseBubble.html', dump=dump)
                bestOffenseBubble = bubbleChartPlotter.best_offensive_teams(savePath + '\\BestOffenseBubble.html', dump=dump)
            except Exception:
                self.logger.info("Failed to plot bubble charts.")
                self.logger.exception("Failed to plot bubble charts.")

                
            #if any more graphs dependent on only standingsDf add here


        if resultsDfLabels is not None and resultsDfList is not None:
            
            #make home wins, away wins and draws pie chart
            try:
                cleanResults = Clean.CleanResults(page) 
                winsDf = cleanResults.make_win_statistics_df()
                title = 'Win Statistics'
                pieChartPlotter = _PieChart._PieChart(title, savePath + '\\WinsPieChart.html') 
                homeAwayWinsPie = pieChartPlotter.make_win_type_chart(winsDf, dump=dump)
            except:
                self.logger.info("Failed to plot home wins, away wins and draws pie chart.")
                self.logger.exception("Failed to plot home wins, away wins and draws pie chart.")
            
            #make line plot of points scored by teams in home and away games
            #this returns list not str like other plotters, jic i forget
            try:
                tempPath = savePath + '\\teams'
                if not os.path.exists(tempPath):
                    os.makedirs(tempPath)
                linePlotter = _LinePlot._LinePlot()
                homeAwayPointsLinePlotsByTeams = linePlotter.make_all_teams_points_scored_plot(resultsDfLabels, resultsDfList, tempPath, dump)
            except:
                self.logger.info("Failed to plot line plot for points scored by teams in home and away games.")
                self.logger.exception("Failed to plot line plot for points scored by teams in home and away games.")

            #heatMap = _HeatMap._HeatMap()
            #heatMap.win_lose_margin_heatmap(resultsDfLabels, resultsDfList)
            
            #add more graphs here which only use resultsDfLabels and resultsDfList here
            
        
        if resultsDfLabels is not None and resultsDfList is not None and standingsDf is not None:

            #make bar chart for home and away goals by teams
            try:
                title = '#Home and #Away Goals Scored by Teams'
                barPlotter = _BarPlot._BarPlot(title, savePath + '\\HomeAwayBar.html')
                homeAwayGoalsBar = barPlotter.make_home_away_goals_chart(resultsDfLabels, resultsDfList, standingsDf, dump=dump)
            except:
                self.logger.info("Failed to plot bar chart for home and away goals scored by teams")
                self.logger.exception("Failed to plot bar chart for home and away goals scored by teams")
            
            #add more graphs here which uses both resultsDfLabels, resultsDfList and standingsDf


        report = Report._Report(leagueCode, season)

        #standingsBoxPlot, homeAwayWinsPie, winLosePercentTeamsPie, homeAwayGoalsBar, gdHistogram, goalsDistPlot
        report.collect_content(
            standingsBoxPlot, 
            homeAwayWinsPie, 
            winLosePercentTeamsPie, 
            homeAwayGoalsBar, 
            goalsDifferenceHisto, 
            goalsNormalDistPlot,
            topScorersGoalsLinePlot,
            bestDefenseBubble,
            bestOffenseBubble,
            homeAwayPointsLinePlotsByTeams
        )

        report.make_report()
        report.save_report()
