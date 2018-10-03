import logging

import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot



class _BarPlot:
    '''Plot various Bar Plots
    '''


    def __init__(self, title:str, location:str):
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

        self.title = title
        self.location = location

        self.logger.debug(f'Title = {self.title}')
        self.logger.debug(f'Location = {self.location}')

        self.logger.info(f'Initializing {__name__} complete..!')



    def make_home_away_goals_chart(self, labels:list, resultsDfList:list, standingsDf:pd.DataFrame):
        '''[summary]
        
        Arguments:
            labels {list} -- [description]
            resultsDfList {list} -- [description]
            standingsDf {pd.DataFrame} -- [description]
        '''

        standings = standingsDf.copy()
        totalGoals = standings['GF'].tolist()
        standings.set_index('Team', inplace=True)

        resultsDfDict = dict(zip(labels, resultsDfList))
        #print(resultsDfDict)
        homeGoals = [resultsDfDict[team].loc['GF'].sum() for team in standingsDf['Team'].tolist()]

        awayGoals = [value - homeGoals[index]  for index, value in enumerate(totalGoals)]

        #labels also need to be reordered according to standings
        labels = standingsDf['Team'].tolist()
        print(homeGoals)
        print(awayGoals)

        #need to list the reverse list here because of plotly's behaviour of plotting top values below
        homeGoals = homeGoals[::-1]
        awayGoals = awayGoals[::-1]
        labels = labels[::-1]

        #actual plotting
        trace1 = go.Bar(
            #y=['giraffes', 'orangutans', 'monkeys'],
            y= labels,
            x=homeGoals,
            name='Home Goals',
            orientation = 'h',
            marker = dict(
                color = 'rgba(78, 80, 212, 1.0)',
                line = dict(
                    color = 'rgba(78, 80, 212, 1.0)',
                    width = 3)
            )
        )

        trace2 = go.Bar(
            #y=['giraffes', 'orangutans', 'monkeys'],
            y = labels,
            #x=[12, 18, 29],
            x = awayGoals,
            name='Away Goals',
            orientation = 'h',
            marker = dict(
                color = 'rgba(93, 227, 83, 1.0)',
                line = dict(
                    color = 'rgba(93, 227, 83, 1.0)',
                    width = 3)
            )
        )

        data = [trace1, trace2]
        layout = go.Layout(
            barmode='stack',
            title=self.title,
            margin=go.layout.Margin(
                l=250,
                r=50,
                b=100,
                t=100,
           ),
           font = {
                    'family' : 'Roboto, monospace',
                    'color' : '#006600',
                    'size' : 15
            },
            plot_bgcolor = '#cce6ff',
            paper_bgcolor = '#ccffff',
        )

        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename=self.location)



    
    




    