from scrape import CategoryScraper, ResultMatrixScraper, LeagueTableScraper



allSeasons = (CategoryScraper.CategoryScraper()).get_league_seasons('ll')
#print(allSeasons['2017–18 Premier League'])
results = (ResultMatrixScraper.ResultMatrixScraper()).get_result_matrix(allSeasons['1929–30 La Liga'])
#print(results)
standings = (LeagueTableScraper.LeagueTableScraper()).get_league_table(allSeasons['1929–30 La Liga'])
print(standings)
