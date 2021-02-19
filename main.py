import os
if os.name=='nt': #windows
    shell='cmd /c '
    clr='cls'
    pyt=''
elif os.name=='posix': #linux/mac
    shell=''
    clr='clear'
    pyt='python3 '
print("Checking modules")
os.system(shell+'pip3 install IMDbPY mysql-connector pyfiglet')
os.system(shell+clr)
import imdb
import mysql.connector as sq
import pyfiglet as fg

sql_host = str(input("Enter database host (or press Enter to use 'localhost'): ")) or "localhost"
sql_id = str(input("Enter database UID (or press Enter to use 'root'): ")) or "root"
sql_pass = str(input("Enter database Password (or press Enter to use 'toor'): ")) or "toor"
sql_db = str(input("Enter database name (or press Enter to use 'imdb'): ")) or "imdb"

db=sq.connect(host=sql_host,user=sql_id,passwd=sql_pass)
cursor=db.cursor()
moviesdb=imdb.IMDb()

def check_db_tb(db_name):
    qu_db_crt='create database '+db_name+';'
    qu_tb_crt='create table movies (id int UNIQUE, movie_name varchar(255), year int, rating float, directors longtext, cast longtext, plot longtext, genre mediumtext);'
    qu_db_chk='show databases;'
    qu_tb_chk='show tables;'
    print("Checking database...")
    cursor.execute(qu_db_chk)
    l = cursor.fetchall()
    l = [i[0] for i in l]
    if not db_name in l:
        print("Database doesn't exist\nCreating database")
        cursor.execute(qu_db_crt)
        db.commit()
    else:
        print("\nDatabase found!")
        cursor.execute('use '+db_name)
    print("Checking table...")
    cursor.execute(qu_tb_chk)
    m = cursor.fetchall()
    m = [i[0] for i in m]
    if not 'movies' in m:
        print("Table doesn't exist\nCreating table")
        cursor.execute(qu_tb_crt)
        db.commit()
    else:
        print("\nTable found!")

check_db_tb(sql_db)
os.system(shell+clr)

def movie_search_online(name):
    global search, num
    num=0
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

def movie_search_offline(name,x,visibility):
    global offline_id,num1
    num1 = 0
    query = "select id,movie_name,year from movies where movie_name like ('%"+name+"%');"
    cursor.execute(query)
    offline_db=cursor.fetchall()
    if visibility==True:
        for i in offline_db:
            num1+=1
            print(num1,".",i[1],"-",i[2])
    elif visibility==False:
        offline_id=offline_db[x-1][0]
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
        print(fg.figlet_format(title_offline,"slant"), "\nYear:", str(year_offline), "\n\nRating:", str(rating_offline), "\n\nPlot Details: "+str(plot_offline), "\n\nDirectors: "+str(directors_offline), "\n\nCast: "+str(cast_offline), "\n\nGenre: "+str(genre_offline))
        print("\nPress any key to continue...")
        return

def database_stock():
    query = "SELECT movie_name,year FROM movies;"
    num2=0
    cursor.execute(query)
    stock=cursor.fetchall()
    for i in stock:
        num2+=1
        print(num2,".",i[0],"-",i[1])
    return

banner=fg.figlet_format("Movie Search")
divider="--------------------------------------"
options="1. Search for a movie\n2. Download a movie to the database\n3. Show movies in offline database\n4. Exit\n"
while True:
    print(banner)
    print(divider)
    print("Choose the following options to continue: \n")
    print(options)
    opt=int(input("Enter your choice: ") or -1)
    os.system(shell+clr)
    if opt==1:
        while True:
            print(fg.figlet_format("Search","slant"))
            print(divider)
            name=str(input("Enter the movie you want to search (or enter 0 to go back to main menu): "))
            print(divider)
            if name=='':
                print('Please enter a movie name! (Press any key to try again!)')
                input()
                os.system(shell+clr)
            elif name=="0":
                os.system(shell+clr)
                break
            else:
                os.system(shell+clr)
                print("You searched: "+name)
                if movie_offline_check(name)==True:
                    while True:
                        print("Movie already exists in offline database")
                        print(divider)
                        movie_search_offline(name, 0, visibility=True)
                        print(">> Enter 0 to go back")
                        print(divider)
                        movie_choice=int(input("Enter the movie number: ") or -1)
                        if movie_choice>num1 or movie_choice==-1:
                            print("Choice doesn't exist, press any key to try again")
                            input()
                            os.system(shell+clr)
                        elif movie_choice==0:
                            os.system(shell+clr)
                            break
                        elif movie_choice<=num1:
                            os.system(shell+clr)
                            movie_search_offline(name, movie_choice, visibility=False)
                            movie_detail_offline(offline_id)
                            input()
                            os.system(shell+clr)
                elif movie_offline_check(name)==False:
                    while True:
                        print("Searching movie online")
                        print(divider)
                        movie_search_online(name)
                        print(">> Enter 0 to go back")
                        print(divider)
                        movie_choice=int(input("Enter the movie number: ") or -1)
                        if movie_choice>num or movie_choice==-1:
                            print("Choice doesn't exist, press any key to try again")
                            input()
                            os.system(shell+clr)
                        elif movie_choice==0:
                            os.system(shell+clr)
                            break
                        elif movie_choice<=num:
                            os.system(shell+clr)
                            movie_detail_online(movie_choice)
                            print(fg.figlet_format(title,"slant"), "\nYear: ", str(year), "\n\nRating: ", str(rating),"\n\nPlot Details: " + str(plot) + "\n\nDirectors: " + str(directors) + "\n\nCast: " + str(cast) + "\n\nGenre: " + str(genre))
                            print("\nPress any key to continue...")
                            input()
                            os.system(shell+clr)
    elif opt==2:
        while True:
            print(fg.figlet_format("Download", "slant"))
            print(divider)
            name=str(input("Enter the movie you want to search and download (or enter 0 to go back to main menu): "))
            print(divider)
            if name=='':
                print('Please enter a movie name! (Press any key to try again!)')
                input()
                os.system(shell+clr)
            elif name=="0":
                os.system(shell+clr)
                break
            else:
                os.system(shell+clr)
                print("You searched: " + name)
                if movie_offline_check(name) == True:
                    print("Movie already exists in offline database")
                    print(divider)
                    movie_search_offline(name, 0, visibility=True)
                    print(divider)
                    print("Press any key to continue...")
                    input()
                    os.system(shell+clr)
                elif movie_offline_check(name) == False:
                    while True:
                        print("Searching movie online")
                        print(divider)
                        movie_search_online(name)
                        print(">> Enter 0 to return to main menu")
                        print(divider)
                        movie_choice = int(input("Enter the movie number: ") or -1)
                        uniq, title, year, rating, directors, cast, plot, genre = [None]*8
                        if movie_choice>num or movie_choice==-1:
                            print("Choice doesn't exist, press any key to try again")
                            input()
                            os.system(shell+clr)
                        elif movie_choice==0:
                            os.system(shell+clr)
                            break
                        elif movie_choice<=num:
                            movie_detail_online(movie_choice)
                            print(divider)
                            movie_store()
                            os.system(shell+clr)
    elif opt==3:
        print(fg.figlet_format("Database", "slant"))
        print(divider)
        print("Showing movies stored in offline database")
        print(divider)
        database_stock()
        print(divider)
        print("Press any key to return to Main Menu")
        input()
        os.system(shell+clr)
    elif opt==4:
        print(fg.figlet_format("Thank You", "slant"))
        print("Press and key to exit...")
        cursor.close()
        db.close()
        input()
        break
    elif opt==-1 or opt>4:
        print(divider)
        print("Wrong choice, try again! (Press Enter to continue)")
        input()
        os.system(shell+clr)