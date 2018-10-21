import logging
import os
from shutil import copyfile

from bs4 import BeautifulSoup





class StyleThemer:
    '''Makes appropriately styled css file for each league'''



    def __init__(self, leagueCode:str):

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info('-----------------------------------------------------------------------------------')
        self.logger.info(f"Initializing {__name__} for '{leagueCode}'.")
        self.logger.info('Initialization complete..!')


        plColors = {'accent':'#3d1958', 'text':'#606060'}
        llColors = {'accent':'#00aa00', 'text':'#000000'}
        saColors = {'accent':'#0068a8', 'text':'#000000'}
        blColors = {'accent':'#d3010c', 'text':'#000000'}
        

        if leagueCode == 'pl':
            self.selectedColors = plColors
        elif leagueCode == 'll':
            self.selectedColors = llColors
        elif leagueCode == 'sa':
            self.selectedColors = saColors
        else:
            self.selectedColors = blColors
        
        logging.debug(self.selectedColors)



    def make_style(self):
        '''Make style and save it into a .css file'''

        style = f'''
        .boxedHeading {{
            border: 1px solid {self.selectedColors['accent']};
            background-color: {self.selectedColors['accent']};
            font-size: 60px;
            text-align: center;
            color:{self.selectedColors['text']};
            font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif   
        }}

        .boxedHeadingFiller {{
        border: 1px solid {self.selectedColors['accent']};
        background-color: {self.selectedColors['accent']};
        font-size: 40px;
        color:{self.selectedColors['accent']};  
        }}

        .boxed {{
        border: 1px solid {self.selectedColors['accent']};
        background-color: {self.selectedColors['accent']};
        font-size: 40px;
        color: {self.selectedColors['text']};
        }}

        .collapse {{
        cursor: pointer;
        display: block;
        border: 1px solid {self.selectedColors['accent']};
        background-color: {self.selectedColors['accent']};
        font-size: 40px;
        color: {self.selectedColors['text']};
        }}

        .collapse + input {{
        display: none; /* hide the checkboxes */
        }}

        .collapse + input + div {{
        display:none;
        }}

        .collapse + input:checked + div {{
        display:block;
        }}

        body {{
            background-color: #363636
        }}

        .boxPlotSize {{
            height: 720px;
            width: 1280px;
        }}

        .homeAwayBarPlotSize {{
            height: 720px;
            width: 1280px;
        }}

        .gdBarPlotSize {{
            height: 800px;
            width: 800px;
        }}

        .bubblePlotSize {{
            height: 450px;
            width: 650px;
        }}

        .distPlotSize {{
            height: 600px;
            width: 1000px;
        }}

        .topScorersLinePlotSize {{
            height: 450px;
            width: 650px;
        }}

        .teamsPerformanceLinePlotSize {{
            height: 1100;
            width: 850;
        }}

        .winTypePiePlotSize {{
            height: 400;
            width: 400;
        }}

        .standingsDonutPiePlotSize {{
            height: 1280;
            width: 720;
        }}
        '''

        self.logger.info('Style creation complete..!')
        return style





class _Report:
    '''Makes report for premier league'''



    def __init__(self, leagueCode:str, seasonName:str):

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info('-----------------------------------------------------------------------------------')
        
        self.logger.info(f"Initializing {__name__} for '{seasonName}'.")
        
        self.seasonName = seasonName
        self.leagueCode = leagueCode

        self.logger.info(f'Getting style for {self.leagueCode}')
        style = StyleThemer(leagueCode)
        self.style = style.make_style()

        self.logger.info('Initialization complete..!')



    def collect_content(self, standingsBoxPlot, homeAwayWinsPie, winLosePercentTeamsPie, 
                        homeAwayGoalsBar, gdHistogram, goalsDistPlot,topScorersGoalsLinePlot,
                        bestDefenseBubble, bestOffenseBubble, homeAwayPointsLinePlotsByTeams):
        '''Initialize the graphs
        '''

        #no need to do this.. 
        #just get plotly graph into divs

        #read BoxPlot.html content
        '''
        with open(f'.\\dumps\\graphs\\pl\\{self.seasonName}\\BoxPlot.html', 'r') as b:
            content = b.read()
            soup = BeautifulSoup(content, features='lxml')
            self.boxPlot = soup.text
            self.boxPlot = self.boxPlot[0:118]
            #print(self.boxPlot)
        '''


        #need to replace to plotly div class with my custom div class
        #class="plotly-graph-div"
        #could have done if checking in other way but doing it in not None way to keep it readable

        if standingsBoxPlot is not None:
            standingsBoxPlot = standingsBoxPlot.replace('plotly-graph-div', 'boxPlotSize')
        self.standingsBoxPlot = standingsBoxPlot

        if homeAwayWinsPie is not None:
            homeAwayWinsPie = homeAwayWinsPie.replace('plotly-graph-div', 'winTypePiePlotSize')
        self.homeAwayWinsPie = homeAwayWinsPie

        if winLosePercentTeamsPie is not None:
            winLosePercentTeamsPie = winLosePercentTeamsPie.replace('plotly-graph-div', 'standingsDonutPiePlotSize')
        self.winLosePercentTeamsPie = winLosePercentTeamsPie

        if homeAwayGoalsBar is not None:
            homeAwayGoalsBar = homeAwayGoalsBar.replace('plotly-graph-div', 'homeAwayBarPlotSize')
        self.homeAwayGoalsBar = homeAwayGoalsBar

        if gdHistogram is not None:
            gdHistogram = gdHistogram.replace('plotly-graph-div', 'gdBarPlotSize')
        self.gdHistogram = gdHistogram

        if goalsDistPlot is not None:
            goalsDistPlot = goalsDistPlot.replace('plotly-graph-div', 'distPlotSize')
        self.goalsDistPlot = goalsDistPlot

        if topScorersGoalsLinePlot is not None:
            topScorersGoalsLinePlot = topScorersGoalsLinePlot.replace('plotly-graph-div', 'topScorersLinePlotSize')
        self.topScorersGoalsLinePlot = topScorersGoalsLinePlot

        if bestDefenseBubble is not None:
            bestDefenseBubble = bestDefenseBubble.replace('plotly-graph-div', 'bubblePlotSize')
        self.bestDefenseBubble = bestDefenseBubble

        if bestOffenseBubble is not None:
            bestOffenseBubble = bestOffenseBubble.replace('plotly-graph-div', 'bubblePlotSize')
        self.bestOffenseBubble = bestOffenseBubble

        
        if homeAwayPointsLinePlotsByTeams is not None:        
            #homeAwayPointsLinePlotsByTeams = homeAwayPointsLinePlotsByTeams.replace('plotly-graph-div', 'boxPlotSize')
            #this is list of graphs.. so need to use comprehension here
            self.homeAwayPointsLinePlotsByTeams = [linePlot.replace('plotly-graph-div', 'teamsPerformanceLinePlotSize') for linePlot in homeAwayPointsLinePlotsByTeams]
        self.homeAwayPointsLinePlotsByTeams = homeAwayPointsLinePlotsByTeams
        


    def make_report(self):

        self.report = f'''
        <!DOCTYPE html>
        <html>

            <head>
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                <style>
                    {self.style}
                </style>
            </head>


            <body>
                <div class="boxedHeadingFiller">-----</div>
                <div class="boxedHeading"><b>{self.seasonName}</b></div>
                <div class="boxedHeadingFiller">-----</div>'''


        self.create_general_insights()
        self.create_match_outcome_analysis()
        self.create_goals_scored_summary()
        self.create_top_goal_scorers()
        self.create_team_performance_line_plot()
                
                
        closingHTML = f'''

            </body>

        </html>'''

        self.report += closingHTML

    

    def create_general_insights(self):
        '''create general insights part of report'''


        openingDiv = f'''
                <br><br><br><br><br><br><br><br><br>
                
                <!---------------------------------------------------------------------------------------->
                <label class="collapse" for="_1">General Insights</label>
                <input id="_1" type="checkbox">
                <div align="center">'''

        self.report += openingDiv


        if self.standingsBoxPlot is not None:

            standingsBoxPlotHTML = f'''    
                    <b> Boxplot </b>
                    {self.standingsBoxPlot}'''
                     
            self.report += standingsBoxPlotHTML
        

        if self.bestDefenseBubble is not None:

            bestDefenseBubbleHTML = f'''
                    <b> Teams with Best Defense </b> 
                    {self.bestDefenseBubble}'''

            self.report += bestDefenseBubbleHTML
        

        if self.bestOffenseBubble is not None:
            
            bestOffenseBubbleHTML = f'''
                    <b> Teams with Best Offense </b>
                    {self.bestOffenseBubble}'''
            
            self.report += bestOffenseBubbleHTML
        
        closingDiv = '''
                </div>'''
        
        self.report +=closingDiv
    


    def create_match_outcome_analysis(self):
        '''Create match outcome analysis part of report'''


        openingDiv = f'''
                <br><br><br><br><br><br><br><br><br>
                
                <!---------------------------------------------------------------------------------------->
                <label class="collapse" for="_2">Match Outcome Analysis</label>
                <input id="_2" type="checkbox">
                <div align="center">'''

        self.report += openingDiv


        if self.homeAwayWinsPie is not None:

            homeAwayWinsPieHTML = f'''    
                    <b> Home/Away Wins </b>
                    {self.homeAwayWinsPie}'''
                     
            self.report += homeAwayWinsPieHTML
        

        if self.winLosePercentTeamsPie is not None:

            winLosePercentTeamsPieHTML = f'''    
                    <b> Overall Wins percent by teams </b>
                    {self.winLosePercentTeamsPie}'''
                     
            self.report += winLosePercentTeamsPieHTML


        closingDiv = '''
                </div>'''
        
        self.report +=closingDiv
    


    def create_goals_scored_summary(self):
        '''Create goals scored summary part of report
        '''


        openingDiv = f'''
                <br><br><br><br><br><br><br><br><br>
                
                <!---------------------------------------------------------------------------------------->
                <label class="collapse" for="_3">Summary for Goals Scored</label>
                <input id="_3" type="checkbox">
                <div align="center">'''

        self.report += openingDiv


        if self.gdHistogram is not None:

            gdHistogramHTML = f'''    
                    <b> Goals Difference by teams </b>
                    {self.gdHistogram}'''
                     
            self.report += gdHistogramHTML
        

        if self.homeAwayGoalsBar is not None:

            homeAwayGoalsBarHTML = f'''    
                    <b> Home/Away goals by teams </b>
                    {self.homeAwayGoalsBar}'''
                     
            self.report += homeAwayGoalsBarHTML
        

        if self.goalsDistPlot is not None:

            goalsDistPlotHTML = f'''
                    <b> Normal Distribution for GF (Goals For), GA (Goals Against) and GD (Goals Against) </b>
                    {self.goalsDistPlot}'''
            
            self.report += goalsDistPlotHTML


        closingDiv = '''
                </div>'''
        
        self.report +=closingDiv


    
    def create_top_goal_scorers(self):
        '''Create top goal scorers part of report
        '''

        if self.topScorersGoalsLinePlot is not None:

            topGoalScorersHTML = f'''
                <br><br><br><br><br>

                <label class="collapse" for="_4">Top Goal Scorers</label>
                <input id="_4" type="checkbox">
                <div align="center">{self.topScorersGoalsLinePlot}</div>'''

            self.report += topGoalScorersHTML



    def create_team_performance_line_plot(self):
        '''Create team wise performance line plot part of report
        '''

        if self.homeAwayPointsLinePlotsByTeams is not None:

            homeAwayPointsLinePlotsByTeamsHTML = f'''
                <br><br><br><br><br>

                <label class="collapse" for="_5">Individual Performance by Teams </label>
                <input id="_5" type="checkbox">
                <div align="center"><br><br><br>{' '.join([f"<div align='center'>{plot}</div><br><br><br>" for plot in self.homeAwayPointsLinePlotsByTeams])}</div>'''
            
            self.report += homeAwayPointsLinePlotsByTeamsHTML



    def save_report(self):
        '''Save report at '.\\dumps\\reports\\{leagueCode}\\{seasonName}'
        '''

        location = f'.\\dumps\\reports\\{self.leagueCode}'


        #if directories doesn't exist create it.. 
        if not os.path.exists(location):
            os.makedirs(location)
        
        '''
        #need to dump to styles.css only once (for first pl report)
        #same style will work for all other reports
        if not os.path.isfile(location + '\\styles.css'):

            
            #styles = None
            #with open('styles.css', 'r') as s:
            #    styles = s.readlines()
            
            #with open(location + '\\styles.css', 'w') as s:
            #    s.write(styles)
            
            #there's already standard library for this don't need to do it manually
            copyfile('.\\templates\\SingleSeason\\pl\\styles.css', location + '\\styles.css')
        '''


        with open(location + f'\\{self.seasonName}.html', 'w') as report:
            report.write(self.report)
