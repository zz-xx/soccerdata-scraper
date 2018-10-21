import logging
from pprint import pprint as pprint

import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.offline import plot
from plotly import tools



class _LinePlot:
    '''Plot various line plots
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



    def  make_top_scorers_goals_plot(self, page:dict, savePath:str, dump):
        '''Make line plot of top scorers of league
        
        Arguments:
            page {dict} -- dictionary of scraped data
        '''
        
        #get list of Top Scorers from page dict
        goals = page['Top Scorers']

        #goals is list of dict
        goals = [g['goals'] for g in goals]

        #goals are already in descending order, need their positions now for plot
        positions = list(range(1, len(goals) + 1))

        
        #text = [f"{pos['goals']} Goals\n {[f'{names['player']} ({names['club']]})" for names in pos['scorers'] ]}' for pos in page['Top Scorers']]
        #text = [f"{pos['goals']} Goals\n" for pos in page['Top Scorers']]
        
        #create hover info containing name and club of goal scorers
        #idk why syntax error when using comprehension inside join method lol
        #need to use <br> instead of '\n' always forget this lol
        text = [f"<b>{pos['goals']} Goals</b><br>" + ' '.join(f"{names['player']} ({names['club']})<br>" for names in pos['scorers']) for pos in page['Top Scorers']]

        # Create a trace
        trace = go.Scatter(
            x = positions,
            y = goals,
            text = text,
            hoverinfo = 'text',
            marker = dict(
                color = 'green'
            ),
        )

        data = [trace]

        layout = go.Layout(
            title = 'Goals Scored by Top Scorers<br>(Hover for info)',
            height = 450,
            width = 650,
            xaxis = {'title' : 'Position'},
            yaxis = {'title' : 'No. of Goals Scored'},
            plot_bgcolor = '#ffffcc',
            paper_bgcolor = '#9999ff'
        )

        fig = go.Figure(data=data, layout=layout)

        if dump is True:
            plot(fig, filename=savePath, auto_open=False, show_link=False)
        
        divPlot = plot(fig, show_link=False, include_plotlyjs=False, output_type='div')
        return divPlot



    def make_all_teams_points_scored_plot(self, resultsDfLabels:list, resultsDfList:str, savePath:str, dump):
        '''[summary]
        
        Arguments:
            resultsDfLabels {list} -- [description]
            resultsDfList {str} -- [description]
            savePath {str} -- [description]
            dump {[type]} -- [description]
        '''

        divPlotList = []

    
        for index, label in enumerate(resultsDfLabels):

            #first make home points graph
            #operate one df at a time

            #make copy of resultsDfList and resultsDfLabels copy
            resultsDfLabelsCopy1 = resultsDfLabels.copy()
            resultsDfListCopy1 = resultsDfList.copy()
            
            header = resultsDfLabelsCopy1.pop(index)
            df = resultsDfListCopy1[index]
            
            #team cannot play against itself also value of the column of this header is nan
            del df[header]

            #points are at y axis
            points = []

            #values which will later be replaced with team labels are x axis
            #we need 
            values = list(range(1, len(resultsDfLabels)))

            #pprint(df)
            #print(resultsDfLabelsCopy1)

            #text to show after hovering
            text = []
            totalPoints = 0

            #3 points for win, 1 for draw 0 for loss
            for team in resultsDfLabelsCopy1:

                #home team won so add 3
                if df.loc['GF'][team] > df.loc['GA'][team]:
                    totalPoints += 3
                    points += [totalPoints]
                    t = f"<b>{header} {df.loc['GF'][team]}</b> - {df.loc['GA'][team]} {team}<br>Took all 3 Points<br>Total {totalPoints} Points"
                    text.append(t)
                
                #game draw so add 1
                elif df.loc['GF'][team] == df.loc['GA'][team]:
                    totalPoints += 1
                    points += [totalPoints]
                    t = f"{header} {df.loc['GF'][team]} - {df.loc['GA'][team]} {team}<br>Missed 2 points<br>Total {totalPoints} Points"
                    text.append(t)
                
                #home team lost so add 0
                else:
                    totalPoints += 0
                    points += [totalPoints]
                    t = f"{header} {df.loc['GF'][team]} - <b>{df.loc['GA'][team]} {team}</b><br>Missed all 3 points<br>Total {totalPoints} Points"
                    text.append(t)
    
            #print(text)
            #print(points)
            #print(totalPoints)
            #print(values)


            #plot away goals line plot
            resultsDfLabelsCopy2 = resultsDfLabels.copy()
            resultsDfListCopy2 = resultsDfList.copy()
        
    
            resultsDfLabelsCopy2.pop(index)
            #print(resultsDfLabelsCopy2)
            #we dont need this df anyway cause team cannot play against itself
            resultsDfListCopy2.pop(index)
            #print(resultsDfListCopy2)

            #print()

            points1 = []
            text1 = []
            totalPoints1 = 0

            for index1, df in enumerate(resultsDfListCopy2):

                #it's opposite here, if GA is greater then away team wins
                
                if df.loc['GA'][label] > df.loc['GF'][label]:
                    totalPoints1 += 3
                    points1 += [totalPoints1]
                    t = f"<b>{label} {int(df.loc['GA'][label])}</b> - {int(df.loc['GF'][label])} {resultsDfLabelsCopy2[index1]}<br>Took all 3 Points<br>Total {totalPoints1} Points"
                    text1.append(t)
                
                #game draw so add 1
                elif df.loc['GA'][label] == df.loc['GF'][label]:
                    totalPoints1 += 1
                    points1 += [totalPoints1]
                    t = f"{label} {int(df.loc['GA'][label])} - {int(df.loc['GF'][label])} {resultsDfLabelsCopy2[index1]}<br>Missed 2 points<br>Total {totalPoints1} Points"
                    text1.append(t)
                
                #home team lost so add 0
                else:
                    totalPoints1 += 0
                    points1 += [totalPoints1]
                    t = f"{label} {int(df.loc['GA'][label])} - <b>{int(df.loc['GF'][label])} {resultsDfLabelsCopy2[index1]}</b><br>Missed all 3 points<br>Total {totalPoints1} Points"
                    text1.append(t)
                
            #print(text1)
            #print(points1)
            #print(totalPoints1)
            print(len(values))
            print(len(points))
            print(len(text))

            #Create trace1
            trace1 = go.Scatter(
                x = values,
                y = points,
                text = text,
                hoverinfo = 'text',
                marker = dict(
                    color = '#FF6037'
                ),
            )

            #Create trace2
            trace2 = go.Scatter(
                x = values,
                y = points1,
                text = text1,
                hoverinfo = 'text',
                marker = dict(
                    color = '#66FF66'
                ),
            )
             
            title1 = f'Points scored by {header} at Home Games<br>(Hover for info)'
            title2 = f'Points scored by {header} at Away Games<br>(Hover for info)'
            fig = tools.make_subplots(rows=2, cols=1, subplot_titles=(title1, title2))

            fig.append_trace(trace1, 1, 1)
            fig.append_trace(trace2, 2, 1)
            #data = [trace1, trace2]

            layout = go.Layout(
                #title = f'Points scored by {header} at Home Games<br>(Hover for info)',
                #title = label,
                height = 1100,
                #650
                width = 850,
                xaxis = {'tickvals' : values, 'ticktext' : resultsDfLabelsCopy1, 'tickangle' : -58},
                yaxis = {'title' : 'Points'},
                xaxis2 = {'tickvals' : values, 'ticktext' : resultsDfLabelsCopy2, 'tickangle' : -58},
                yaxis2 = {'title' : 'Points'},
                margin=go.layout.Margin(
                    t=62,
                    b=140,
                    l=65,
                    r=50
                ),
                showlegend=False,
                plot_bgcolor = '#50BFE6',
                paper_bgcolor = '#FF00CC'
            )

            #fig = go.Figure(data=data, layout=layout)
            fig['layout'].update(layout)
            config = {'displayModeBar': False}

            if dump is True:
                plot(fig, filename=savePath + f'\\{label}.html', auto_open=False)#, config=config)
            
            divPlot = plot(fig, show_link=False, include_plotlyjs=False, output_type='div', config=config)
            divPlotList.append(divPlot)
        
        return divPlotList
