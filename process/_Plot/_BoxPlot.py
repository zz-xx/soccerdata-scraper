import logging

import plotly.graph_objs as go
from plotly.offline import plot



class _BoxPlot:
    '''Plot various Box Plots
    '''


    def __init__(self, title:str, labels:list, values:list, location:str):
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
        self.labels = labels
        self.values = values
        self.location = location

        self.logger.debug(f'Title = {self.title}')
        self.logger.debug(f'Labels = {self.labels}')
        self.logger.debug(f'Values = {self.values}')
        self.logger.debug(f'Location = {self.location}')

        self.logger.info(f'Initializing {__name__} complete..!')



    def make_box_plot(self, subplot=False):
        '''Make the box plot and store it at location
        '''

        x_data = self.labels
        y_data = self.values

        #can take random colors but will leave it at this for now
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
            
            title=self.title,
            #width=1280,
            #height=720,
            autosize=True,
            yaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=True,
                dtick=5,
                gridcolor='#7f7f7f',
                gridwidth=0.5,
                zerolinecolor='rgb(255, 255, 255)',
                zerolinewidth=2,
            ),
            margin=dict(
                l=40,
                r=30,
                b=80,
                t=100,
            ),
            font = {
                    'family' : 'Roboto, monospace',
                    'color' : '#006600',
                    'size' : 15
            },
            plot_bgcolor = '#cce6ff',
            paper_bgcolor = '#ccffff',
            showlegend=True
        )

        fig = go.Figure(data=traces, layout=layout)

        if subplot is True:
            return layout, traces
        
        plot(fig, filename=self.location)


    





