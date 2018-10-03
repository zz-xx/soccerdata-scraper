import logging

import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot



class _PieChart:
    '''Plot various Pie Charts
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



    def make_win_type_chart(self, wins:pd.DataFrame):
        '''Make pie chart showing home wins, away wins and draws for a season
        
        Arguments:
            wins {pd.DataFrame} -- home, away wins and draws data
        '''

        #skipping first since it's total games
        labels = list(wins.columns.values)[1:]
        values = list(wins.values.tolist()[0])[1:]
    
        colors = ['#4dff88', '#b380ff', '#ff9933', '#4dff88']
        trace = go.Pie(labels=labels, values=values,
                       hoverinfo='label+percent', textinfo='value', 
                       textfont=dict(size=20),
                       marker=dict(colors=colors, 
                       line=dict(color='#000000', width=2)))

        layout = go.Layout(
            title=self.title,
            width=400,
            height=400,
            font = {
                    'family' : 'Roboto, monospace',
                    'color' : '#006600',
                    'size' : 12
            },
            plot_bgcolor = '#cce6ff',
            paper_bgcolor = '#ccffff',
            showlegend=True
        )

        fig = go.Figure(data=[trace], layout=layout)
        plot(fig, filename=self.location)



    def make_standings_donut_chart(self, standings:pd.DataFrame):
        '''Makes a pie chart showing win and lose percent of each team from total games
        
        Arguments:
            standings {pd.DataFrame} -- dataframe containing final league standings
        '''

        fig = {
            "data": [
                {
                "values": standings['W'].tolist(),
                "labels": standings['Team'].tolist(),
                "domain": {"x": [0, .48]},
                "name": "Wins",
                "hoverinfo":"label+percent+name",
                "hole": .4,
                "type": "pie"
                },
                {
                "values": standings['L'].tolist(),
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
                    "title":"Total Win and Loss % by teams",
                    #'width': 850,
                    #'height': 500,
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
                            "text": "Loss",
                            "x": 0.8,
                            "y": 0.5
                        }
                    ],
                    'font' : {
                    'family' : 'Roboto, monospace',
                    'color' : '#006600',
                    'size' : 15
                    },
                    'plot_bgcolor' : '#cce6ff',
                    'paper_bgcolor' : '#ccffff',
                }
            }

        plot(fig, filename=self.location)


    

