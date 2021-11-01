# WineXp

WineXp is a Web Application designed for anyone interested in fine wines. It enables users to search for global wine scores (GWS) and global vintage scores (WineXp Vintage Score) in a simple, easy to use, comprehensive interface. 

## Understanding WineXp Scores

### The Global Wine Score (GWS)

The Global Wine Score or GWS is provided by globalwinescore.com API, and it's objective is to bring simplicity and efficiency by delivering a *single score*, aggregated from several expert ratings, allowing the easy comparison of wines made from different grapes and from different regions around the world. 

The algorithm also takes into account that many wines are re-tasted by critics as they age, so the GWS is constantly updated to include the new ratings received for a wine.
For more information on The Global Wine Score and [calculation methods](https://www.globalwinescore.com/calculation/) visit [Global Wine Score](https://globalwinescore.docs.apiary.io/#introduction/authentication) website. 

### The WineXp Vintage Score 

The WineXp Vintage Score is calculated using a sqlite database as data source. The concept is also to offer a simple efficient *single score* aggregated from multiple normalized expert ratings. Allowing instant comparison between vintages for a given region and same vintages from different regions around the world. Every score is aggregated from at least 3 professional publication reviews.

# Basics

## Register/Login
To enter WineXp users are required to log in or register if first time visiting. Once logged in, access to all features is granted and user can choose among Search Wine, Search Vintage, Recent Searches and Logout. 

## Search Wine
When in the *Search Wine* page, users are prompted to input a wine name (optional) and a vintage (optional) which when submitted, the application renders a page that displays the actual *GWS* score for that wine along with some meta-data like, number of *Journalists Reviews* considered on the GWS calculation, *Confidence Index* which is based on the number of samples and their standard deviation, and also the date in which the score was *last updated*.

The page also displays as a bonus, a GWS score for every vintage of the given wine, presented in a ranked by score scrollable table. Additionally, if only a vintage (no wine name) is submitted, the system will return a table showing the *top 100 scored wines* for that vintage. In both cases all items in table are clickable as links to a new search.

## Vintage Charts
When in *Vintage Charts* page, users are presented with a list of wine producing producing countries. Just choose a country and application will present the list of regions of that country. Choose a region and the application will then render a page that displays a table with a *WineXp Vintage Score* and the *drinking window* status for each vintage of the given region. Here all table items are also clickable as links to a new search.

## Recent Searches
Seaches are stored in a sqlite database an the *Recent Searches* page displays into a condensed table, user's last 25 searched wines including it's meta-data. Again, here all items are clickable for a convenient 1-click new search.

## Logout
Clickin at the *Logout* will log out user from session.

# Tech Stack:
Code was designed and organized in a model–view–controller (MVC) pattern using the following technologies: 

Backend:
Python, Flask, GWS API

Frontend:
HTML5 / CSS3 (Bootstrap 4), Javascript

Database:
SQLite

# Credits
WineXp was designed and built by Luis Felipe Klaus for Harvard CS50x 2020 final project.

YouTube [link](https://www.youtube.com/watch?v=jAJx1MTEo84).

For a demo version visit [WineXp](http://winexp-cli.herokuapp.com).
