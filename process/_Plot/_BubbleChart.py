import logging

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot

#from pprint import pprint as pprint



class _BubbleChart:
    '''Plot Bubble Charts
    '''


    def __init__(self, season:str, standingsDf:pd.DataFrame):
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

        self.season = season
        self.standingsDf = standingsDf

        self.logger.info(f'Initializing {__name__} complete..!')
    


    def best_defensive_teams(self, savePath:str, dump):
        '''Makes bubble chart for best defensive teams in given season
        '''

        #make copy so we can sort by value
        standingsDfCopy = self.standingsDf.copy()

        #sort by GA in ascending order to get teams with best defense
        standingsDfCopy.sort_values(by='GA', inplace=True)

        #pprint(standingsDfCopy)
        superScript = ['st', 'nd', 'rd', 'th', 'th']
        text = [f"<b>{team}</b> <br>{standingsDfCopy['GA'].tolist()[index]} goals conceded<br><b>Stands {standingsDfCopy['Pos'].tolist()[index]}<sup>{superScript[index]}</sup></b> in {self.season}" for index, team in enumerate(standingsDfCopy['Team'].tolist()[0:5])]

        trace0 = go.Scatter(
            x=list(range(1,6)),
            y=standingsDfCopy['GA'].tolist()[0:5],
            mode='markers',
            text = text,
            hoverinfo = 'text',
            marker=dict(
                color=['#FAFA37', '#FFAA1D', '#58427C', '#00CC99', '#87421F'],
                opacity=[1, 0.8, 0.6, 0.4, 0.2],
                size=standingsDfCopy['GA'].tolist()[0:5],
            )
        )

        layout = go.Layout(
            title = '5 Best Defensive Teams<br>(Hover for info)',
            height = 450,
            width = 650,
            #xaxis = {'title' : 'Defense Ranking', 'showgrid':False, 'gridcolor':'#bdbdbd', 'gridwidth':0.25, 'linecolor':'#636363', 'linewidth':6},
            #yaxis = {'title' : 'Goals conceded', 'showgrid':False, 'gridcolor':'#bdbdbd', 'gridwidth':0.25, 'linecolor':'#636363', 'linewidth':6},
            xaxis = {'title' : 'Defense Ranking'},
            yaxis = {'title' : 'Goals conceded'},
            plot_bgcolor = '#FDD7E4',
            paper_bgcolor = '#66FF66'
        )

        data = [trace0]
        fig = go.Figure(data=data, layout=layout)

        config = {'displayModeBar': False}
        #plot(fig, filename=savePath, show_link=False, config=config)

        if dump == True:
            plot(fig, filename=savePath, show_link=False, auto_open=False)
        
        divPlot = plot(fig, show_link=False, include_plotlyjs=False, output_type='div', config=config)
        return divPlot




    #well this is literally same as above code except color, title and dataframe column changes
    def best_offensive_teams(self, savePath:str, dump):
        '''Makes bubble chart for best offensive teams in league
        '''

        standingsDfCopy = self.standingsDf.copy()

        #sort by GF in descending order to get teams with best offense
        standingsDfCopy.sort_values(by='GF', inplace=True, ascending=False)

        #pprint(standingsDfCopy)
        superScript = ['st', 'nd', 'rd', 'th', 'th']
        text = [f"<b>{team}</b> <br>{standingsDfCopy['GF'].tolist()[index]} goals scored<br><b>Stands {standingsDfCopy['Pos'].tolist()[index]}<sup>{superScript[index]}</sup></b> in {self.season}" for index, team in enumerate(standingsDfCopy['Team'].tolist()[0:5])]

        trace0 = go.Scatter(
            x=list(range(1,6)),
            y=standingsDfCopy['GF'].tolist()[0:5],
            mode='markers',
            text = text,
            hoverinfo = 'text',
            marker=dict(
                color=['#FFD12A', '#EE34D2', '#92926E', '#2243B6', '#14A989'],
                opacity=[1, 0.8, 0.6, 0.4, 0.2],
                size=standingsDfCopy['GF'].tolist()[0:5],
            )
        )

        layout = go.Layout(
            title = '5 Best Offensive Teams<br>(Hover for info)',
            height = 450,
            width = 650,
            #xaxis = {'title' : 'Defense Ranking', 'showgrid':False, 'gridcolor':'#bdbdbd', 'gridwidth':0.25, 'linecolor':'#636363', 'linewidth':6},
            #yaxis = {'title' : 'Goals conceded', 'showgrid':False, 'gridcolor':'#bdbdbd', 'gridwidth':0.25, 'linecolor':'#636363', 'linewidth':6},
            xaxis = {'title' : 'Offense Ranking'},
            yaxis = {'title' : 'Goals Scored'},
            plot_bgcolor = '#AAF0D1',
            paper_bgcolor = '#FF3855'
        )

        data = [trace0]
        fig = go.Figure(data=data, layout=layout)

        config = {'displayModeBar': False}
        #plot(fig, filename=savePath, show_link=False, config=config)

        if dump == True:
            plot(fig, filename=savePath, show_link=False, auto_open=False)
        
        divPlot = plot(fig, show_link=False, include_plotlyjs=False, output_type='div', config=config)
        return divPlot
