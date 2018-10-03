import logging

import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.offline import plot



class _DistPlot:
    '''Plot various Dist Plots
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

        self.title = title
        self.location = location

        self.logger = logging.getLogger(__name__)
        self.logger.info('-----------------------------------------------------------------------------------')
        self.logger.info(f'Initializing {__name__}.')

    

    def make_normal_goal_distribution(self, standingsDf:pd.DataFrame):
        '''Make dataframe of goals from league table
        
        Arguments:
            standingsDf {pd.DataFrame} -- league table parsed into a pandas DF
        '''

        x1 = standingsDf['GA'].tolist()[::-1] 
        x2 = standingsDf['GF'].tolist()[::-1]
        x3 = standingsDf['GD'].tolist()[::-1]

        hist_data = [x1, x2, x3]

        group_labels = ['GA', 'GF', 'GD']

        colors = ['#00FF00', '#FF3300', '#6E0DD0']
        #colors = ['#00FF00', '#FF3300']

        layout = go.Layout(
            title=self.title,
            width=1000,
            height=600,
            font = {
                    'family' : 'Roboto, monospace',
                    'color' : '#006600',
                    'size' : 12
            },
            plot_bgcolor = '#cce6ff',
            paper_bgcolor = '#ccffff'
        )

        # create distplot with curve_type set to 'normal'
        fig = ff.create_distplot(hist_data, group_labels, show_hist = False, bin_size=.5, curve_type='normal', colors=colors)

        fig.layout.update(layout)

        plot(fig, filename=self.location)
