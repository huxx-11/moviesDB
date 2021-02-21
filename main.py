import os
if os.name == 'nt':  # windows
    shell = 'cmd /c '
    clr = 'cls'
    pyt = ''
elif os.name == 'posix':  # linux/mac
    shell = ''
    clr = 'clear'
    pyt = 'python3 '
print("Checking modules")
os.system(shell + 'pip3 install IMDbPY mysql-connector pyfiglet')
os.system(shell + clr)
import imdb
import mysql.connector as sq
import pyfiglet as fg

moviesdb = imdb.IMDb()

def enable_local_db():
    while True:
        global sql_host, sql_id, sql_pass, sql_db, sql, db, cursor
        sql_host = str(input("Enter database host (or press Enter to use 'localhost'): ")) or "localhost"
        sql_id = str(input("Enter database UID (or press Enter to use 'root'): ")) or "root"
        sql_pass = str(input("Enter database Password (or press Enter to use 'toor'): ")) or "toor"
        sql_db = str(input("Enter database name (or press Enter to use 'imdb'): ")) or "imdb"
        try:
            db = sq.connect(host=sql_host, user=sql_id, passwd=sql_pass)
            cursor = db.cursor()
            break
        except:
            print("Database connection failed! Please check if local instance is running or not, \nand press any key to try again")
            input()
            os.system(shell + clr)


def check_db_tb(db_name):
    qu_db_crt = 'create database ' + db_name + ';'
    qu_tb_crt = 'create table movies (id int UNIQUE, movie_name varchar(255), year int, rating float, directors longtext, cast longtext, plot longtext, genre mediumtext);'
    qu_db_chk = 'show databases;'
    qu_tb_chk = 'show tables;'
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
        cursor.execute('use ' + db_name)
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


while True:
    db_choice = str(input("Do you want to use local MySQL database to store info (Default Y)? [Y/N]: ") or "Y" or "y")
    if db_choice in ["y", "Y"]:
        print("You're using online/offline mode")
        enable_local_db()
        check_db_tb(sql_db)
        break
    elif db_choice in ["n", "N"]:
        print("You're using online only mode'")
        break
    else:
        print("Wrong Choice! Try again")
        input()
        os.system(shell + clr)

os.system(shell + clr)

def movie_search_online(nm):
    global search, num
    num = 0
    search = moviesdb.search_movie(nm)
    for movie in search:
        num += 1
        print(num, ".", movie.get('title'), "-", movie.get('year'))
    return

def movie_detail_online(x):
    m_id = search[x - 1].getID()
    mv = moviesdb.get_movie(m_id)
    global uniq, title, year, rating, directors, cast, plot, genre
    uniq = m_id
    title = mv.get('title')
    year = mv.get('year')
    if mv.get('rating') is None:
        rating = "Not available yet"
    else:
        rating = mv.get('rating')
    if mv.get('directors') is None:
        directors = None
    else:
        directors = ', '.join(map(str, mv.get('directors')))
    if mv.get('cast') is None:
        cast = None
    else:
        cast = ', '.join(map(str, mv.get('cast')))
    if mv.get('plot outline') is None:
        plot = None
    else:
        plot = (mv.get('plot outline')).replace('"', "")
    genre = ', '.join(mv.get('genre'))
    return

def movie_offline_check(x):
    query = "select id from movies where movie_name like ('%" + x + "%');"
    cursor.execute(query)
    id_list = cursor.fetchall()
    if len(id_list) == 0:
        return False
    else:
        return True

def movie_store():
    try:
        query = 'INSERT INTO movies (id,movie_name,year,rating,directors,cast,plot,genre) VALUES (' + str(
            uniq) + ',"' + str(title) + '",' + str(year) + ',' + str(rating) + ',"' + str(directors) + '","' + str(
            cast) + '","' + str(plot) + '","' + str(genre) + '");'
        cursor.execute(query)
        db.commit()
        print("\nMovie details successfully downloaded to offline database")
        print("\nPress any key to continue...")
        input()
    except Exception as e:
        print("Download Error! Please try again\n", e)

def movie_search_offline(m_name, x, visibility):
    global offline_id, num1
    num1 = 0
    query = "select id,movie_name,year from movies where movie_name like ('%" + m_name + "%');"
    cursor.execute(query)
    offline_db = cursor.fetchall()
    if visibility:
        for i in offline_db:
            num1 += 1
            print(num1, ".", i[1], "-", i[2])
    elif not visibility:
        offline_id = offline_db[x - 1][0]
    return

def del_movie(x):
    query_show = "select movie_name,year from movies where id =" + str(x)
    query_del = "delete from movies where id =" + str(x)
    cursor.execute(query_show)
    temp = cursor.fetchall()
    for i in temp:
        del_choice = i[0] + " - " + str(i[1])
    choice = input("Do you want to delete this movie >> " + del_choice + " [Y/N]: ")
    if choice in ["Y", "y"]:
        try:
            cursor.execute(query_del)
            db.commit()
            print(del_choice, "successfully deleted!")
            input()
            return
        except Exception as e:
            print("Deletion error, Please try again!\n", e)
            input()
    elif choice in ["N", "n"]:
        os.system(shell + clr)
        return
    else:
        print("Wrong choice, press any key to try again")
        input()
        os.system(shell + clr)
        return

def movie_detail_offline(x):
    query = "SELECT * FROM movies WHERE id =" + str(x)
    cursor.execute(query)
    movie_details = cursor.fetchall()
    for i in movie_details:
        title_offline = i[1]
        year_offline = i[2]
        rating_offline = i[3]
        directors_offline = i[4]
        cast_offline = i[5]
        plot_offline = i[6]
        genre_offline = i[7]
        print(fg.figlet_format(title_offline, "slant"), "\nYear:", str(year_offline), "\n\nRating:",
              str(rating_offline), "\n\nPlot Details: " + str(plot_offline), "\n\nDirectors: " + str(directors_offline),
              "\n\nCast: " + str(cast_offline), "\n\nGenre: " + str(genre_offline))
        print("\nPress any key to continue...")
        return

def database_stock():
    query = "SELECT movie_name,year FROM movies;"
    num2 = 0
    cursor.execute(query)
    stock = cursor.fetchall()
    for i in stock:
        num2 += 1
        print(num2, ".", i[0], "-", i[1])
    return

def offline_show_menu():
    print("Movie already exists in offline database")
    while True:
        while True:
            try:
                print(divider)
                movie_search_offline(name, 0, visibility=True)
                print(">> Enter 0 to go back")
                print(divider)
                movie_choice = int(input("Enter the movie number: "))
                break
            except:
                print("Choice doesn't exist, press any key to try again")
                input()
                os.system(shell + clr)
        if movie_choice <= num1 and not movie_choice == 0:
            os.system(shell + clr)
            movie_search_offline(name, movie_choice, visibility=False)
            movie_detail_offline(offline_id)
            input()
            os.system(shell + clr)
        elif int(movie_choice) == 0:
            os.system(shell + clr)
            break
        else:
            print("Choice doesn't exist, press any key to try again")
            input()
            os.system(shell + clr)
    return

def online_show_menu():
    while True:
        while True:
            try:
                print("Searching movie online")
                print(divider)
                movie_search_online(name)
                print(">> Enter 0 to go back")
                print(divider)
                movie_choice = int(input("Enter the movie number: "))
                break
            except:
                print("Choice doesn't exist, press any key to try again")
                input()
                os.system(shell + clr)
        if movie_choice <= num and not movie_choice == 0:
            os.system(shell + clr)
            movie_detail_online(movie_choice)
            print(fg.figlet_format(title, "slant"), "\nYear: ", str(year), "\n\nRating: ", str(rating),
                  "\n\nPlot Details: " + str(plot) + "\n\nDirectors: " + str(directors) + "\n\nCast: " + str(
                      cast) + "\n\nGenre: " + str(genre))
            print("\nPress any key to continue...")
            input()
            os.system(shell + clr)
        elif movie_choice == 0:
            os.system(shell + clr)
            break
        elif movie_choice > num:
            print("Choice doesn't exist, press any key to try again")
            input()
            os.system(shell + clr)
    return

def offline_main_menu():
    global name
    while True:
        while True:
            try:
                print(banner)
                print(divider)
                print("Choose the following options to continue: \n")
                print(options)
                opt = int(input("Enter your choice: "))
                break
            except:
                os.system(shell + clr)
                print(divider)
                print("Wrong choice, try again! (Press Enter to continue)")
                input()
                os.system(shell + clr)
        os.system(shell + clr)
        if opt == 1:
            while True:
                print(fg.figlet_format("Search", "slant"))
                print(divider)
                name = str(input("Enter the movie you want to search (or enter 0 to go back to main menu): "))
                print(divider)
                if name == '':
                    print('Please enter a movie name! (Press any key to try again!)')
                    input()
                    os.system(shell + clr)
                elif name == "0":
                    os.system(shell + clr)
                    break
                else:
                    os.system(shell + clr)
                    print("You searched: " + name)
                    if db_choice in ["y", "Y"]:
                        if movie_offline_check(name):
                            offline_show_menu()
                        elif not movie_offline_check(name):
                            online_show_menu()
                    elif db_choice in ["n", "N"]:
                        print("Movie will be searched online only")
                        print(divider)
                        online_show_menu()

        elif opt == 2:
            while True:
                print(fg.figlet_format("Download", "slant"))
                print(divider)
                name = str(
                    input("Enter the movie you want to search and download (or enter 0 to go back to main menu): "))
                print(divider)
                if name == '':
                    print('Please enter a movie name! (Press any key to try again!)')
                    input()
                    os.system(shell + clr)
                elif name == "0":
                    os.system(shell + clr)
                    break
                else:
                    os.system(shell + clr)
                    print("You searched: " + name)
                    if movie_offline_check(name):
                        print("Movie already exists in offline database")
                        print(divider)
                        movie_search_offline(name, 0, visibility=True)
                        print(divider)
                        print("Press any key to continue...")
                        input()
                        os.system(shell + clr)
                    elif not movie_offline_check(name):
                        while True:
                            while True:
                                try:
                                    print("Searching movie online")
                                    print(divider)
                                    movie_search_online(name)
                                    print(">> Enter 0 to return to main menu")
                                    print(divider)
                                    movie_choice = int(input("Enter the movie number: "))
                                    break
                                except:
                                    print("Choice doesn't exist, press any key to try again")
                                    input()
                                    os.system(shell + clr)
                            uniq, title, year, rating, directors, cast, plot, genre = [None] * 8
                            if movie_choice <= num and not movie_choice == 0:
                                movie_detail_online(movie_choice)
                                print(divider)
                                movie_store()
                                os.system(shell + clr)
                            elif movie_choice == 0:
                                os.system(shell + clr)
                                break
                            elif movie_choice > num:
                                print("Choice doesn't exist, press any key to try again")
                                input()
                                os.system(shell + clr)

        elif opt == 3:
            print(fg.figlet_format("Database", "slant"))
            print(divider)
            print("Showing movies stored in offline database")
            print(divider)
            database_stock()
            print(divider)
            print("Press any key to return to Main Menu")
            input()
            os.system(shell + clr)

        elif opt == 4:
            while True:
                while True:
                    try:
                        print(fg.figlet_format("Deletion", "slant"))
                        print(divider)
                        print("Showing movies stored in offline database")
                        print(divider)
                        movie_search_offline('', 0, True)
                        print(">> Enter 0 to go back")
                        print(divider)
                        del_choice = int(input("Enter the movie number you want to delete: "))
                        break
                    except:
                        print("Wrong choice, press any key to try again")
                        input()
                        os.system(shell + clr)
                if del_choice <= num1 and not del_choice == 0:
                    movie_search_offline('', del_choice, False)
                    del_movie(offline_id)
                    os.system(shell + clr)
                elif del_choice == 0:
                    os.system(shell + clr)
                    break
                else:
                    print("Wrong choice, press any key to try again")
                    input()
                    os.system(shell + clr)


        elif opt == 5:
            print(fg.figlet_format("Thank You", "slant"))
            print("Press and key to exit...")
            cursor.close()
            db.close()
            input()
            break

        else:
            print(divider)
            print("Wrong choice, try again! (Press Enter to continue)")
            input()
            os.system(shell + clr)

def online_main_menu():
    global name
    while True:
        while True:
            try:
                print(banner)
                print(divider)
                print("Choose the following options to continue: \n")
                print(options_online)
                opt = int(input("Enter your choice: "))
                break
            except:
                os.system(shell + clr)
                print(divider)
                print("Wrong choice, try again! (Press Enter to continue)")
                input()
                os.system(shell + clr)
        os.system(shell + clr)
        if opt == 1:
            while True:
                print(fg.figlet_format("Search", "slant"))
                print(divider)
                name = str(input("Enter the movie you want to search (or enter 0 to go back to main menu): "))
                print(divider)
                if name == '':
                    print('Please enter a movie name! (Press any key to try again!)')
                    input()
                    os.system(shell + clr)
                elif name == "0":
                    os.system(shell + clr)
                    break
                else:
                    os.system(shell + clr)
                    print("You searched: " + name)
                    if db_choice in ["y", "Y"]:
                        if movie_offline_check(name) == True:
                            offline_show_menu()
                        elif movie_offline_check(name) == False:
                            online_show_menu()
                    elif db_choice in ["n", "N"]:
                        print("Movie will be searched online only")
                        print(divider)
                        online_show_menu()
        elif opt == 2:
            print(fg.figlet_format("Thank You", "slant"))
            print("Press and key to exit...")
            input()
            break

        else:
            print(divider)
            print("Wrong choice, try again! (Press Enter to continue)")
            input()
            os.system(shell + clr)
    return

banner = fg.figlet_format("Movie Search")
divider = "--------------------------------------"
options = "1. Search for a movie\n2. Download a movie to the database\n3. Show movies in offline database\n4. Delete movie from offline database\n5. Exit\n"
options_online = "(Searching online only)\n\n1. Search for a movie\n2. Exit\n"
if db_choice in ["y", "Y"]:
    offline_main_menu()
elif db_choice in ["n", "N"]:
    online_main_menu()
