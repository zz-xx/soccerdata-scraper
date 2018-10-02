import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot



class BoxPlot:
    '''Contains methods for showing various data representation
    '''

    def make_standings_box_plot(self, standingsDfList:list, seasonNames:list):
        '''[summary]
        
        Arguments:
            standingsDfList {list} -- [description]
            seasonNames {list} -- [description]
        '''


        '''
        x_data = ['Carmelo Anthony', 'Dwyane Wade',
                'Deron Williams', 'Brook Lopez',
                'Damian Lillard', 'David West',]
        '''
        x_data = seasonNames

        '''
        y0 = np.random.randn(50)-1
        y1 = np.random.randn(50)+1
        y2 = np.random.randn(50)
        y3 = np.random.randn(50)+2
        y4 = np.random.randn(50)-2
        y5 = np.random.randn(50)+3
        '''

        #for now making for 'GF'

        #y_data = [y0,y1,y2,y3,y4,y5]
        y_data = [np.array(df['W'].tolist()) for df in standingsDfList]

        colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)']

        traces = []

        for xd, yd, cls in zip(x_data, y_data, colors):
                traces.append(go.Box(
                    y=yd,
                    name=xd,
                    boxpoints='all',
                    jitter=0.5,
                    whiskerwidth=0.2,
                    fillcolor=cls,
                    marker=dict(
                        size=2,
                    ),
                    line=dict(width=1),
                ))

        layout = go.Layout(
            title='Boxplot for wins(W) by teams across various seasons',
            yaxis=dict(
                autorange=True,
                showgrid=True,
                zeroline=True,
                dtick=5,
                gridcolor='rgb(255, 255, 255)',
                gridwidth=1,
                zerolinecolor='rgb(255, 255, 255)',
                zerolinewidth=2,
            ),
            margin=dict(
                l=40,
                r=30,
                b=80,
                t=100,
            ),
            paper_bgcolor='rgb(243, 243, 243)',
            plot_bgcolor='rgb(243, 243, 243)',
            showlegend=False
        )

        fig = go.Figure(data=traces, layout=layout)
        plot(fig, filename='name1.html')




class PieChart:


    def make_wins_pie_chart(self, wins:pd.DataFrame):

        #skipping first since it's total games
        self.make_pie_chart(list(wins.columns.values)[1:], list(wins.values.tolist()[0])[1:])



    def make_pie_chart(self, labels:list, values:list):

        colors = ['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1']

        trace = go.Pie(labels=labels, values=values,
                       hoverinfo='label+percent', textinfo='value', 
                       textfont=dict(size=20),
                       marker=dict(colors=colors, 
                       line=dict(color='#000000', width=2)))

        #py.iplot([trace], filename='styled_pie_chart')
        plot([trace], filename='pie.html')

    

    def make_standings_donut_chart(self, standings:pd.DataFrame):
        '''[summary]
        
        Arguments:
            standings {pd.DataFrame} -- [description]
        '''

        fig = {
            "data": [
                {
                #"values": [16, 15, 12, 6, 5, 4, 42],
                "values": standings['W'].tolist(),
                #"labels": ["US","China","European Union","Russian Federation","Brazil","India","Rest of World"],
                "labels": standings['Team'].tolist(),
                "domain": {"x": [0, .48]},
                "name": "Wins",
                "hoverinfo":"label+percent+name",
                "hole": .4,
                "type": "pie"
                },
                {
                #"values": [27, 11, 25, 8, 1, 3, 25],
                "values": standings['L'].tolist(),
                #"labels": ["US","China","European Union","Russian Federation","Brazil","India","Rest of World"],
                "labels": standings['Team'].tolist(),
                "text":["Losses"],
                "textposition":"inside",
                "domain": {"x": [.52, 1]},
                "name": "Losses",
                "hoverinfo":"label+percent+name",
                "hole": .4,
                "type": "pie"
                }],
            "layout": {
                    "title":"Total Win and Lose percent by teams",
                    "annotations": [
                        {
                            "font": {
                                "size": 20
                            },
                            "showarrow": False,
                            "text": "Wins",
                            "x": 0.20,
                            "y": 0.5
                        },
                        {
                            "font": {
                                "size": 20
                            },
                            "showarrow": False,
                            "text": "Losses",
                            "x": 0.8,
                            "y": 0.5
                        }
                    ]
                }
            }
        #py.iplot(fig, filename='donut')
        plot(fig, filename='stpie.html')
    



class BarCharts:


    def make_home_away_goals_chart(self, labels:list, resultsDfList:list, standingsDf:pd.DataFrame):
        '''[summary]
        
        Arguments:
            labels {list} -- [description]
            resultsDfList {list} -- [description]
            totalGoals {list} -- [description]
        '''

        '''
        standings = standingsDf
        homeGoals = [df.loc['GF'].sum() for df in resultsDfList]
        #print(resultsDfList[10].loc['GF'].sum())
        #print(homeGoals)
        #print(labels)

        #since team names in standings are not sorted have to employ this workaround
        standings.set_index('Team', inplace=True)
        #print(standings.loc['West Bromwich Albion']['GF'])        
        totalGoals = [standings.loc[l]['GF'] for l in labels]
        
        #print(totalGoals)
        
        #totalGoals and #homeGoals should be of same len anyway so this will work
        awayGoals = [value - homeGoals[index]  for index, value in enumerate(totalGoals)]

        #print(awayGoals)
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
            margin=go.layout.Margin(
                l=150,
                r=50,
                b=100,
                t=100,
           )
        )

        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename='bar.html')




