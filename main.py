import os
print("Checking modules")
os.system('cmd /c pip install IMDbPY mysql-connector pyfiglet')
os.system('cmd /c cls')
import imdb
import mysql.connector as sq
import pyfiglet as fg

sql_host = str(input("Enter database host (or press Enter to use 'localhost'): ")) or "localhost"
sql_id = str(input("Enter database UID (or press Enter to use 'root'): ")) or "root"
sql_pass = str(input("Enter database Password (or press Enter to use 'toor'): ")) or "toor"
sql_db = str(input("Enter database name (or press Enter to use 'imdb'): ")) or "imdb"
os.system('cmd /c cls')
db=sq.connect(host=sql_host,user=sql_id,passwd=sql_pass,database=sql_db)
cursor=db.cursor()

moviesdb=imdb.IMDb()

def movie_search_online(name):
    num=0
    global search
    search=moviesdb.search_movie(name)
    for movie in search:
        num+=1
        print(num,".",movie.get('title'),"-",movie.get('year'))
    return

def movie_detail_online(x):
    id=search[x-1].getID()
    mv=moviesdb.get_movie(id)
    global uniq, title, year, rating, directors, cast, plot, genre
    uniq=id
    title=mv.get('title')
    year=mv.get('year')
    if mv.get('rating')==None:
        rating = "Not available yet"
    else:
        rating=mv.get('rating')
    if mv.get('directors')==None:
        directors = None
    else:
        directors=', '.join(map(str,mv.get('directors')))
    if mv.get('cast')==None:
        cast = None
    else:
        cast=', '.join(map(str,mv.get('cast')))
    if mv.get('plot outline')==None:
        plot=None
    else:
        plot=(mv.get('plot outline')).replace('"',"")
    genre=', '.join(mv.get('genre'))
    #print(type(title),type(year),type(rating),type(directors),type(cast),type(plot),type(genre))

    return

def movie_offline_check_dep(x):
    cursor.execute("SELECT * FROM movies WHERE id = "+str(x))
    if len(cursor.fetchall())==0:
        return False
    else:
        return True

def movie_offline_check(x):
    query = "select id from movies where movie_name like ('%" + x + "%');"
    cursor.execute(query)
    id_list=cursor.fetchall()
    if len(id_list)==0:
        return False
    else:
        return True

def movie_store():
    query='INSERT INTO movies (id,movie_name,year,rating,directors,cast,plot,genre) VALUES ('+str(uniq)+',"'+str(title)+'",'+str(year)+','+str(rating)+',"'+str(directors)+'","'+str(cast)+'","'+str(plot)+'","'+str(genre)+'");'
    cursor.execute(query)
    db.commit()
    print("\nMovie details successfully downloaded to offline database")
    print("\nPress any key to continue...")
    input()

def movie_search_offline(name):
    num=0
    global offline_id
    query = "select id,movie_name,year from movies where movie_name like ('%"+name+"%');"
    cursor.execute(query)
    offline_db=cursor.fetchall()
    for i in offline_db:
        num+=1
        print(num,".",i[1],"-",i[2])
        offline_id=i[0]
    return

def movie_detail_offline(x):
    query = "SELECT * FROM movies WHERE id ="+str(x)
    cursor.execute(query)
    movie_details=cursor.fetchall()
    for i in movie_details:
        title_offline = i[1]
        year_offline = i[2]
        rating_offline = i[3]
        directors_offline = i[4]
        cast_offline = i[5]
        plot_offline = i[6]
        genre_offline = i[7]
        print(fg.figlet_format(title_offline,"slant"), "Year:", str(year_offline), "\n\nRating:", str(rating_offline), "\n\nPlot Details:"+str(plot_offline), "\n\nDirectors:"+str(directors_offline), "\n\nCast:"+str(cast_offline), "\n\nGenre:"+str(genre_offline))
        print("\nPress any key to continue...")
        return

def database_stock():
    query = "SELECT movie_name,year FROM movies;"
    num=0
    cursor.execute(query)
    stock=cursor.fetchall()
    for i in stock:
        num+=1
        print(num,".",i[0],"-",i[1])
    return

banner=fg.figlet_format("Movie Search")
divider="------------------------------"
options="1. Search for a movie\n2. Store a movie in the database\n3. Show movies in offline database\n4. Exit\n"
while True:
    print(banner)
    print(divider)
    print("Choose the following options to continue: \n")
    print(options)
    opt=int(input("Enter your choice: "))
    os.system('cmd /c cls')
    if opt==1:
        name=input("Enter the movie you want to search: ")
        print(divider)
        print("You searched: "+name)
        if movie_offline_check(name)==True:
            print("Movie already exists in offline database")
            print(divider)
            movie_search_offline(name)
            print(divider)
            movie_choice=int(input("Enter the movie number: "))
            os.system('cmd /c cls')
            movie_detail_offline(offline_id)
            input()
            os.system('cmd /c cls')
        elif movie_offline_check(name)==False:
            print("Searching movie online")
            print(divider)
            movie_search_online(name)
            print(divider)
            movie_choice=int(input("Enter the movie number: "))
            os.system('cmd /c cls')
            movie_detail_online(movie_choice)
            print(fg.figlet_format(title,"slant"), "Year:", str(year), "\n\nRating:", str(rating),"\n\nPlot Details: " + str(plot) + "\n\nDirectors: " + str(directors) + "\n\nCast: " + str(cast) + "\n\nGenre: " + str(genre))
            print("\nPress enter to continue...")
            input()
            os.system('cmd /c cls')
    elif opt==2:
        name=input("Enter the movie you want to search and store: ")
        print(divider)
        print("You searched: " + name)
        if movie_offline_check(name) == True:
            print("Movie already exists in offline database\nPress any key to continue")
            print(divider)
            input()
            os.system('cmd /c cls')
        elif movie_offline_check(name) == False:
            print("Searching movie online")
            print(divider)
            movie_search_online(name)
            print(divider)
            movie_choice = int(input("Enter the movie number: "))
            uniq, title, year, rating, directors, cast, plot, genre = [None]*8
            movie_detail_online(movie_choice)
            print(divider)
            movie_store()
            os.system('cmd /c cls')
    elif opt==3:
        print("Showing movies stored in offline database")
        print(divider)
        database_stock()
        print(divider)
        print("Press any key to return to Main Menu")
        input()
        os.system('cmd /c cls')
    elif opt==4:
        print(divider)
        print("Exiting...")
        cursor.close()
        db.close()
        break
    else:
        print(divider)
        print("Wrong choice, try again! (Press Enter to continue)")
        input()
        os.system('cmd /c cls')