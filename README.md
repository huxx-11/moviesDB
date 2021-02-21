# moviesDB [CLI]
<p align="center"><img src="app_icon.ico" alt="moviesDB"/></p>

## Get all your movie details in one place! Works on IMDb API
# Requirements
 - Windows (x64) / Linux / macOS 10.11+
 - Python3 - https://www.python.org/downloads/ (Optional)
 - MySQL Community Server - https://dev.mysql.com/downloads/mysql/ (Optional)

## Usage
> For full functionality, don't run using IDLE or any other Python IDE.
> Run via terminal (Linux/macOS) or cmd/ps (Windows)

> Or, get executable files from [releases](https://github.com/strider-one/moviesDB/releases) [Recommended]

*It automatically initializes the required database and table, on initial run*

## Features
**You can choose Online-only mode or Online/Offline mode, at the startup of the app**

Shows **Title, Year, Rating, Directors, Cast, Plot and Genre** when searching movie details

Shows **Name, Nicknames, Birth Date, Birth Place, Biography and Filmography** when searching cast details

 1. Search for movie details online
 2. Search for cast details online
 3. Download/Delete movie details to/from MySQL database *(only if using online/offline mode)*
 4. Show the downloaded movie list and also their details *(only if using online/offline mode)*

## Screenshots
Main menu (Online/Offline mode)
![Main Menu](https://i.ibb.co/C6csr8T/Screenshot-2021-02-20-022027.png)

Movie search demo
![Movie search demo](https://i.ibb.co/ZT93pX8/Screenshot-2021-02-20-022209.png)

## Modules Used
1. mysql-connector - https://pypi.org/project/mysql-connector/
2. IMDbPY - https://pypi.org/project/IMDbPY/
3. pyfiglet - https://pypi.org/project/pyfiglet/
