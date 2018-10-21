import logging

import numpy as np
import pandas as pd
import plotly.figure_factory as ff
from plotly.offline import plot

from pprint import pprint as pprint



class _HeatMap:
    '''Plot Heat Maps
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



    def win_lose_margin_heatmap(self, resultsDfLabels:list, resultsDfList:list):
        '''Make heatmap showing winning and losing margins of a team at home and away games
        '''

        #make copy of resultsDfList df's
        #resultsDfListCopy = resultsDfList.copy()
        #generic copy makes shallow copy so it doesnt works on nested lists lol
        #so need to use list.deepcopy() but it comes with pretty big performance hit
        #so sticking with good old comprehensions

        resultsDfListCopy = [x[:] for x in resultsDfList]
        #del resultsDfListCopy[0][resultsDfLabels[0]]

        #work on the copy now
        resultsDfListCopy[0].loc['GD'] = resultsDfListCopy[0].loc['GF'] - resultsDfListCopy[0].loc['GA']

        #sort_values entire dataframe by GD row (axis=1 is column wise)
        resultsDfListCopy[0].sort_values(by='GD', axis=1, inplace=True)
        print(resultsDfListCopy[0])

        self.logger.debug(f'resultsDfListCopy={resultsDfListCopy}')

        
        z = [resultsDfListCopy[0].loc['GD'].tolist()]
        print(len(z))

        x = list(resultsDfListCopy[0].columns.values)
        y = [resultsDfLabels[0]]

        #ternary statement lol
        z_text = ['Win' if gd > 0 else 'draw' if gd == 0 else 'Lose' for gd in resultsDfListCopy[0].loc['GD'].tolist()]
        print(len(z_text))

        fig = ff.create_annotated_heatmap(z, x=None, y=y, annotation_text=[z_text], colorscale='Viridis', showscale=True)
        plot(fig, filename='annotated_heatmap_text')
        



