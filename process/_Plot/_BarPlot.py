import logging

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot

#from pprint import pprint as pprint


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



    def make_home_away_goals_chart(self, labels:list, resultsDfList:list, standingsDf:pd.DataFrame, dump:bool):
        '''[summary]
        
        Arguments:
            labels {list} -- [description]
            resultsDfList {list} -- [description]
            standingsDf {pd.DataFrame} -- [description]
            bool -- [description]
        '''

        standings = standingsDf.copy()
        totalGoals = standings['GF'].tolist()
        standings.set_index('Team', inplace=True)

        resultsDfDict = dict(zip(labels, resultsDfList))
        #print(resultsDfDict)


        #major bug here if trying to arrange in standings order because of mismatch of labels 
        #in results and standings, can't help it much except keeping alternative way ready
        #specially for old bundesliga so need to keep long performance inefficient approach
        homeGoals = None
        awayGoals = None
        #labels = None

        try:
            homeGoals = [resultsDfDict[team].loc['GF'].sum() for team in standingsDf['Team'].tolist()]

            awayGoals = [value - homeGoals[index]  for index, value in enumerate(totalGoals)]

            #labels also need to be reordered according to standings
            labels = standingsDf['Team'].tolist()
            #print(homeGoals)
            #print(awayGoals)

        except:
            self.logger.info('Keyerror bug detected. Trying alternative approach.')

            #now have to manually count all goals scored through results df which is pain
            #also the histogram will now be in alphabetical order instead of standings table order
            #doesn't matter much but standings order is better way to represent imo
            #pprint(resultsDfList)
            homeGoals = [resultsDfList[index].loc['GF'].sum() for index in range(0,len(labels))]

            #len of labels and resultsdf should be same so no need to do explicit check
            #if it's not then something else is wrong which is not here
            #'-' was already replaced by np.nan while cleaning so np.nansum can be done 
            #this is probably most convenient way to get sum without one more extra loop
            awayGoals = [np.nansum(np.array([df.loc['GA'][team] for df in resultsDfList])) for team in labels] 
            #print(homeGoals)
            #print(awayGoals)
            #print([a+homeGoals[i] for i,a in enumerate(awayGoals)])
            

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
            height=720, width=1280,
            
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
            paper_bgcolor = '#ccffff'
        )

        fig = go.Figure(data=data, layout=layout)

        if dump == True:
            plot(fig, filename=self.location, auto_open=False)
        
        divPlot = plot(fig, show_link=False, include_plotlyjs=False, output_type='div')
        return divPlot



    def  make_gd_chart(self, standingsDf:pd.DataFrame, dump):
        '''Make a bar chart showing goal differences across teams
        
        Arguments:
            standingsDf {pd.DataFrame} -- [description]
        '''

        x = standingsDf['GD'].tolist()[::-1]
        y = standingsDf['Team'].tolist()[::-1]
        
        #for hover info
        text = [f"<b>{team}</b><br>Goals For: {standingsDf['GF'].tolist()[::-1][index]}<br>Goals Against: {standingsDf['GA'].tolist()[::-1][index]}<br>Goals Difference: {x[index]}" for index, team in enumerate(y)]

        data = [
            go.Bar(
                x=x,
                y=y,
                text = text,
                hoverinfo = 'text',
                marker=dict(
                    #color='rgb(102, 255, 153)',
                    color='#FF0099',
                    line=dict(color='rgb(0, 0, 0)',
                            width=2)
                ),
                orientation='h',
            )
       ]

        layout = go.Layout(
            autosize=False, height=800, width=800,
            bargap=0.15, bargroupgap=0.1,
            barmode='stack', hovermode='x',
            margin=dict(r=30, l=225,
                        b=75, t=125),
            title=self.title,
            xaxis=dict(
                dtick=10, nticks=0,
                gridcolor='rgb(102, 255, 153)',
                linecolor='#000', linewidth=1,
                mirror=True,
                showticklabels=True, tick0=0, tickwidth=1,
                title='<i>Goals Difference(GD)</i>',
            ),
            yaxis=dict(
                anchor='x',
                gridcolor='rgb(102, 255, 153)', gridwidth=1,
                linecolor='#000', linewidth=1,
                mirror=True, showgrid=False,
                showline=True, zeroline=False,
                showticklabels=True, tick0=0,
                type='category',
            ),
            font = {
                    'family' : 'Roboto, monospace',
                    'color' : '#006600',
                    'size' : 15
            },
            plot_bgcolor = '#cce6ff',
            paper_bgcolor = '#ccffff'
        )

        fig = go.Figure(data=data, layout=layout)

        if dump == True:
            plot(fig, filename=self.location, auto_open=False)
        
        divPlot = plot(fig, show_link=False, include_plotlyjs=False, output_type='div')
        return divPlot
  