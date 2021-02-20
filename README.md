# moviesDB [CLI]
## Get all your movie details in one place! Works on IMDb API
<p align="center"><img src="app_icon.ico" alt="moviesDB"/></p>

# Requirements
 - Windows (x64) / Linux / macOS 10.11+
 - Python3 - https://www.python.org/downloads/
 - MySQL Community Server - https://dev.mysql.com/downloads/mysql/

## Usage
Windows:
> Run the file directly
> or, browse using cmd/ps to the directory and run > python main.py

Linux / macOS
> Browse to the directory using terminal and run > python3 main.py 

*It automatically initializes the required database and table, on initial run*

## Features
Shows **Title, Year, Rating, Directors, Cast, Plot and Genre**

 1. Search for movie details online
 2. Download movie details to MySQL database
 3. Show the downloaded movie list and also their details

## Screenshots
Main menu
![Main Menu](https://i.ibb.co/C6csr8T/Screenshot-2021-02-20-022027.png)

Movie search demo
![Movie search demo](https://i.ibb.co/ZT93pX8/Screenshot-2021-02-20-022209.png)

## Modules Used
1. mysql-connector - https://pypi.org/project/mysql-connector/
2. IMDbPY - https://pypi.org/project/IMDbPY/
3. pyfiglet - https://pypi.org/project/pyfiglet/
