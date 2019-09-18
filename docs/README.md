# Basic Overview
_soccerdata-scraper_ scrapes soccer data from ***Wikipedia*** across tier 1 European Football Leagues and makes interactive as well as interesting data visualizations from it. 

Current available leagues for *scraping* and then visualizations are given below.

<table>
  
  <tr>
  <td><b>League</b></td>
  <td><b>Seasons</b></td>
  <td><b>Source</b></td>
  </tr>
   
  <tr>
  <td>English Premier League</td>
  <td>1992-93 to <i>present</i></td>
  <td>https://en.wikipedia.org/wiki/Category:Premier_League_seasons</td>
  </tr>
  
  <tr>
  <td>Spanish La Liga</td>
  <td>1929-30 to <i>present</i></td>
  <td>https://en.wikipedia.org/wiki/Category:La_Liga_seasons</td>
  </tr>
  
  <tr>
  <td>Italian Serie A</td>
  <td>1929-30 to <i>present</i></td>
  <td>https://en.wikipedia.org/wiki/Category:Serie_A_seasons</td>
  </tr>
  
  <tr>
  <td>German Bundesliga</td>
  <td>1963-64 to <i>present</i></td>
  <td>https://en.wikipedia.org/wiki/Category:Bundesliga_seasons</td>
  </tr>
  
</table>


# Requirements
Install the dependencies listed below manually or use _requirements.txt_
> pip install -r requirements.txt

List of libraries apart from standard ones that are required to make soccerdata-scraper work correctly. Use of ***Python 3.7.x*** or higher and most recently available stable builds for libraries is recommended.

## [bs4](https://pypi.org/project/beautifulsoup4/)
Beautiful Soup is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.

## [requests](https://pypi.org/project/requests/)
Requests is an elegant and simple HTTP library for Python, built for human beings.

## [numpy](https://pypi.org/project/numpy/)
NumPy is the fundamental package for array computing with Python.

## [pandas](https://pypi.org/project/pandas/)
Powerful data structures for data analysis, time series, and statistics

## [plotly](https://pypi.org/project/plotly/)
An open-source, interactive graphing library for Python

## [cefpython3](https://pypi.org/project/cefpython3/)
GUI toolkit for embedding a Chromium widget in desktop applications

## [PIL](https://pypi.org/project/Pillow/)
Python Imaging Library


# Usage

After making sure all dependencies are installed correctly, execute _main.py_. If everything's right, a graphical interface window should pop up.

1. Press _START_. ![](https://github.com/zz-xx/soccerdata-scraper/blob/master/media/GUI1.PNG)

2. Select a league from top bar. ![](https://github.com/zz-xx/soccerdata-scraper/blob/master/media/GUI2.PNG)

3. Click on _Select Season_ drop down. ![](https://github.com/zz-xx/soccerdata-scraper/blob/master/media/GUI.png)


# Output

![](/media/outwindow.PNG?raw=true) A new window should open up which contains interactive visualizations for selected season's data. Click on sub headings in this window to expand them and view the respective visualizations inside them. All generated graphs can be interacted within this window. A complete sample interactive visualization report which was shown here, can be can be seen _here_.

Also all the visualization reports generated are stored in a _html_ file and can be interacted again through a web browser or if only some visualizations are required, they are also stored separately in a _html_ file and can be retrieved individually. Along with this all the scraped data is further parsed into a _JSON_ file and stored, should you only need the data and not visualizations.

A new folder called _dumps_ should appear in soccerdata-scraper directory or whatever you have named current directory. Its contents will be something like this. 
![](https://github.com/zz-xx/soccerdata-scraper/blob/master/media/dumps.PNG)

All three folders will contains 4 sub folders one for each league. 
![](https://github.com/zz-xx/soccerdata-scraper/blob/master/media/league.PNG)

Contents of _graphs_ folder look something like this, after selecting a league. 
![](https://github.com/zz-xx/soccerdata-scraper/blob/master/media/graphleagues.PNG)

After selecting the respective season folder, individual visualizations can be interacted with.
![](https://github.com/zz-xx/soccerdata-scraper/blob/master/media/graphleaguefolder.PNG)

Contents of _json_ folder after selecting a league look something like this.  All the data used for visualization can be obtained from this files. 
![](https://github.com/zz-xx/soccerdata-scraper/blob/master/media/jsonfolder.PNG)

_reports_ folder contains the all complete season wise interactive visualization reports for each league, as seen through our interface. It's contents after selecting a league should look something like this. 
![](https://github.com/zz-xx/soccerdata-scraper/blob/master/media/reportsfolder.PNG)


## Note
While this has been extensively tested, some specific visualizations for some seasons might fail due to page changes or some other reasons. Even in such possibility, visualizations should still work for whatsoever data that was scraped and parsed without any issues.


