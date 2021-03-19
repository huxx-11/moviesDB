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
os.system(shell + 'pip3 install IMDbPY mysql-connector pyfiglet pillow requests')
os.system(shell + clr)
import imdb
import mysql.connector as sq
import pyfiglet as fg
import questionary

banner = fg.figlet_format("Movie Search")
divider = "--------------------------------------"
options = "1. Search for a movie\n2. Search for cast\n3. Download a movie to the database\n4. Show movies in offline database\n5. Delete movie from offline database\n6. Exit\n"
options_online = "(Searching online only)\n\n1. Search for a movie\n2. Search for cast\n3. Exit\n"

moviesdb = imdb.IMDb()

#ENABLE/DISABLE LOCAL DATABASE FUNCTION
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
            return True
        except:
            print(
                "Database connection failed! Please check if local instance is running or not, \nand press any key to try again")
            input()
            os.system(shell + clr)
            return False

#DATABASE AND TABLE CHECK FUNCTION
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
    return

def useDB():
    global db_choice
    while True:
        db_choice = str(input("Do you want to use local MySQL database to store info (Default N)? [Y/N]: ") or "N" or "n")
        if db_choice in ["y", "Y"]:
            print("You're using online/offline mode")
            if enable_local_db():
                check_db_tb(sql_db)
                break
            else:
                pass
        elif db_choice in ["n", "N"]:
            print("You're using online only mode'")
            break
        else:
            print("Wrong Choice! Try again")
            input()
            os.system(shell + clr)

#ONLINE MOVIE SEARCH POPULATOR FUNCTION
def movie_search_online(nm):
    global filtered_dict, num
    show_dict = {}
    filtered_dict = {}
    num = 0
    search = moviesdb.search_movie(nm)
    for i in search:
        show_dict.update({i.getID():(i.get('title'),str(i.get('year')))})
    for j in show_dict:
        if not show_dict[j] in list(filtered_dict.values()):
            filtered_dict.update({j:show_dict[j]})
    for movie in list(filtered_dict.values()):
        num += 1
        print(num, ".", movie[0], "-", movie[1])
    return

#ONLINE MOVIE DETAILS FUNCTION
def movie_detail_online(x):
    m_id = list(filtered_dict)[x-1]
    mv = moviesdb.get_movie(m_id)
    global uniq, title, year, rating, directors, cast, plot, genre, cover
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
    if mv.get('genre') is None:
        genre = None
    else:
        genre = ', '.join(mv.get('genre'))
    if mv.get('full-size cover url') is None:
        cover = None
    else:
        cover = mv.get('full-size cover url')
    return

#OFFLINE MOVIE SEARCH POPULATOR FUNCTION
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

#OFFLINE DB MOVIE DETAILS FUNCTION
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

#OFFLINE DB CHECK FUNCTION
def movie_offline_check(x):
    query = "select id from movies where movie_name like ('%" + x + "%');"
    cursor.execute(query)
    id_list = cursor.fetchall()
    if len(id_list) == 0:
        return False
    else:
        return True

#DOWNLOADER FUNCTION
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

#DELETE FROM OFFLINE DB FUNCTION
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

#DB STOCK FUNCTION
def database_stock():
    query = "SELECT movie_name,year FROM movies;"
    num2 = 0
    cursor.execute(query)
    stock = cursor.fetchall()
    for i in stock:
        num2 += 1
        print(num2, ".", i[0], "-", i[1])
    return

#CAST SEARCH POPULATOR FUNCTION
def person_search(actor_name):
    global num_actor,actor_list
    num_actor=0
    actor_list=moviesdb.search_person(actor_name)
    for actor in actor_list:
        num_actor+=1
        print(num_actor,".", actor.get('name'), "- IMDb ID:", actor.personID)
    return

#CAST SEARCH DETAILS FUNTION
def person_details(x):
    global actor_id, ac_name, ac_nick, ac_birthp, ac_dob, ac_bio, ac_films, mv_counter, ac_url
    mv_counter=0
    ac_films=[]
    actor_id=actor_list[x-1].getID()
    actor_details=moviesdb.get_person(actor_id)
    ac_name=actor_details['name']
    try:
        ac_nick=', '.join(actor_details['nick names'])
    except:
        ac_nick="None"
    try:
        ac_dob = actor_details['birth date']
    except:
        ac_dob = "Not found"
    try:
        ac_birthp = actor_details['birth notes']
    except:
        ac_birthp="Not found"
    try:
        ac_bio = ', '.join(actor_details['mini biography'])
    except:
        ac_bio="No biography found"
    try:
        ac_url = actor_details.get('full-size headshot')
    except:
        ac_url = None
    try:
        for i in actor_details['filmography']:
            if i in ['actor','actress']:
                gender=i
        if actor_details['filmography'][gender] == None:
            ac_films="No films found"
        else:
            for films in (actor_details['filmography'][gender]):
                mv_counter+=1
                try:
                    mv_year=films['year']
                except:
                    mv_year=''
                ac_films.append((str(mv_counter)+". "+str(films)+" - "+str(mv_year)))
    except:
        ac_films = "No films found"
    return

#OFFLINE DB MOVIE MENU FUNCTION
def offline_show_menu(name):
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

#ONLINE MOVIE MENU FUNCTION
def online_show_menu(name):
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
            while True:
                while True:
                    print(fg.figlet_format(title, "slant"), "\nYear: ", str(year), "\n\nRating: ", str(rating),
                    "\n\nPlot Details: " + str(plot) + "\n\nDirectors: " + str(directors) + "\n\nCast: " + str(
                    cast) + "\n\nGenre: " + str(genre))
                    try:
                        cov_show=input("\nPress Enter to view cover art [or enter 0 to go back]: ")
                        break
                    except:
                        print("Wrong choice!Press any key to try again!")
                        input()
                if cov_show == '':
                    show_cover(cover,title)
                    print("Showing cover art")
                elif cov_show=='0':
                    break
                else:
                    print("Wrong choice!Press any key to try again!")
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

#SEARCH FOR A MOVIE MENU FUNCTION
def search_movie_menu():
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
                    offline_show_menu(name)
                elif not movie_offline_check(name):
                    online_show_menu(name)
            elif db_choice in ["n", "N"]:
                print("Movie will be searched online only")
                print(divider)
                online_show_menu(name)
    return

#SEARCH FOR CAST MENU FUNCTION
def search_cast_menu():
    while True:
        print(fg.figlet_format("Cast", "slant"))
        print(divider)
        name = str(input("Enter the name of actor/actress you want to search (or enter 0 to go back to main menu): "))
        print(divider)
        if name == '':
            print('Please enter some name! (Press any key to try again!)')
            input()
            os.system(shell + clr)
        elif name == "0":
            os.system(shell + clr)
            break
        else:
            while True:
                while True:
                    os.system(shell + clr)
                    print("You searched for: " + name + "\nShowing matches")
                    print(divider)
                    person_search(name)
                    print(">> Enter 0 to go back")
                    print(divider)
                    try:
                        choice_p = int(input("Select the number: "))
                        os.system(shell + clr)
                        break
                    except:
                        print("Wrong choice, press any key to try again")
                        input()
                        os.system(shell + clr)
                if choice_p <= num_actor and not choice_p == 0:
                    person_details(choice_p)
                    while True:
                        print(fg.figlet_format(ac_name, "slant"), "\nNick Names:", ac_nick, "\n\nBirth Date:", ac_dob,
                              "\n\nBirth Place", ac_birthp, "\n\nBiography:", ac_bio, )
                        print(divider)
                        while True:
                            try:
                                film_choice = int(input("\nPress Enter to show filmography\nEnter 1 to view Picture (or Enter 0 to go back): "))
                                break
                            except:
                                film_choice = "show"
                                break
                        if film_choice == "show":
                            os.system(shell + clr)
                            print("Filmography of ", ac_name)
                            print(divider)
                            print('\n'.join(map(str, ac_films)))
                            print(divider + '\nPress any key to go back...')
                            input()
                            os.system(shell + clr)
                            pass
                        elif film_choice == 1:
                            show_cover(ac_url, ac_name)
                            print("Showing picture")
                        elif film_choice == 0:
                            os.system(shell + clr)
                            break
                elif choice_p == 0:
                    break
                else:
                    print("Wrong choice, press any key to try again")
                    input()
    return

#DOWNLOAD A MOVIE TO DATABASE FUNCTION
def download_menu():
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
    return

#SHOW MOVIES IN OFFLINE DATABASE FUNCTION
def database_menu():
    print(fg.figlet_format("Database", "slant"))
    print(divider)
    print("Showing movies stored in offline database")
    print(divider)
    database_stock()
    print(divider)
    print("Press any key to return to Main Menu")
    input()
    os.system(shell + clr)
    return

#DELETE MOVIE FROM OFFLINE DATABASE FUNCTION
def delete_menu():
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
    return

#OFFLINE MAIN MENU FUNCTION
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
            search_movie_menu()
        elif opt == 2:
            search_cast_menu()
        elif opt == 3:
            download_menu()
        elif opt == 4:
            database_menu()
        elif opt == 5:
            delete_menu()
        elif opt == 6:
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

#ONLINE MAIN MENU FUNCTION
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
            search_movie_menu()
        elif opt == 2:
            search_cast_menu()
        elif opt == 3:
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

#MOVIE/CAST COVER FUNCION
def show_cover(url,name):
    if url is None:
        print("Cover image not found! Press any key to continue...")
    else:
        import tkinter as tk
        from PIL import ImageTk, Image
        import requests
        from io import BytesIO
        root = tk.Tk()
        root.geometry("450x675")
        root.title(name)
        #root.iconbitmap('app_icon.ico')
        response = requests.get(url)
        img_data = response.content
        basewidth = 450
        res_img = Image.open(BytesIO(img_data))
        wpercent = (basewidth / float(res_img.size[0]))
        hsize = int((float(res_img.size[1]) * float(wpercent)))
        display = res_img.resize((basewidth, hsize), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(display)
        panel = tk.Label(root, image=img, bd=0)
        panel.pack(side="bottom", fill="both", expand="yes")
        root.mainloop()
        return

useDB()
if db_choice in ["y", "Y"]:
    offline_main_menu()
elif db_choice in ["n", "N"]:
    online_main_menu()