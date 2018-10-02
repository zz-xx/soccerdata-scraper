import logging

from scrape import Category, Page
from process import Clean, Plot



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('-----------------------------------------------------------------------------------')
logger.info(f'Initializing {__name__}.')

league = 'pl'
season = '2017–18 Premier League'

logger.info('Getting available seasons..')
seasons = (Category.Category()).get_league_seasons(league)
logger.info('Recieved seasons..!')

logger.info(f"Scraping data from page '{season}'...")
page = (Page.Page(season, league, seasons)).get_data(dump=True)
logger.info('Scraped data successfully..!')


'''
#for making multiple box plots

dfList = []
labelList = []
standingsDf = (Clean.CleanStandings(page)).make_df()
print(standingsDf)
dfList.append(standingsDf)
labelList.append(season)

season = '2013–14 Premier League'
page = (Page.Page(season, league, seasons)).get_data(dump=True)
standingsDf = (Clean.CleanStandings(page)).make_df()
print(standingsDf)
dfList.append(standingsDf)
labelList.append(season)

season = '2014–15 Premier League'
page = (Page.Page(season, league, seasons)).get_data(dump=True)
standingsDf = (Clean.CleanStandings(page)).make_df()
print(standingsDf)
dfList.append(standingsDf)
labelList.append(season)

season = '2015–16 Premier League'
page = (Page.Page(season, league, seasons)).get_data(dump=True)
standingsDf = (Clean.CleanStandings(page)).make_df()
print(standingsDf)
dfList.append(standingsDf)
labelList.append(season)

season = '2016–17 Premier League'
page = (Page.Page(season, league, seasons)).get_data(dump=True)
standingsDf = (Clean.CleanStandings(page)).make_df()
print(standingsDf)
dfList.append(standingsDf)
labelList.append(season)

#request problem with this specific page
#season = '2012–13 Premier League'
#page = (Page.Page(season, league, seasons)).get_data(dump=True)
#standingsDf = (Clean.CleanStandings(page)).make_df()
#print(standingsDf)
#dfList.append(standingsDf)
#labelList.append(season)


season = '2011–12 Premier League'
page = (Page.Page(season, league, seasons)).get_data(dump=True)
standingsDf = (Clean.CleanStandings(page)).make_df()
print(standingsDf)
dfList.append(standingsDf)
labelList.append(season)

(Plot.BoxPlot()).make_standings_box_plot(dfList, labelList)
'''

#winsDf = (Clean.CleanResults(page)).make_win_statistics_df()
#print(winsDf.values.tolist())
#print(winsDf.columns.values)
#(Plot.PieChart()).make_wins_pie_chart(winsDf)

'''
#for making donut chart of season
standingsDf = (Clean.CleanStandings(page)).make_df()
(Plot.PieChart()).make_standings_donut_chart(standingsDf)
'''

labels, resultsDfList = (Clean.CleanResults(page)).make_results_df()
#print(titles)
#print(resultsDfList)
standingsDf = (Clean.CleanStandings(page)).make_df()
#print(standingsDf)
(Plot.BarCharts()).make_home_away_goals_chart(labels, resultsDfList, standingsDf)











