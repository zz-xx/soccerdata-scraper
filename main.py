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


(Plot.Plot()).plot_single_season_report(page, season, league, seasons)
