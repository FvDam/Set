import sqlite3 as sq
import time


def check_func(func):
    def wrapper_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (sq.OperationalError, sq.IntegrityError):
            print(f"{func.__name__} returns an error, please try again with another id or value.")
            return None
    return wrapper_func


class DataBase():
    def __init__(self):
        self.conn = sq.connect("my_database.db")
        self.curs = self.conn.cursor()
        self.curs.execute("PRAGMA foreign_keys=ON")

        self.curs.execute("""CREATE TABLE IF NOT EXISTS player_table 
                                (player_id varchar(20) PRIMARY KEY);""")

        
        self.curs.execute("""CREATE TABLE IF NOT EXISTS game_table 
                                    (game_id        INTEGER PRIMARY KEY,
                                    player_id       varchar(20),
                                    total_time      INT NOT NULL,
                                    score           INT NOT NULL,
                                    wrong           INT NOT NULL,
                                    correct         INT NOT NULL,
                                    FOREIGN KEY(player_id) REFERENCES player_table(player_id));""")

        self.curs.execute("""CREATE TABLE IF NOT EXISTS time_table 
                                (time_id INTEGER PRIMARY KEY,
                                    game_id         INTEGER NOT NULL,
                                    time_begin      INT NOT NULL,
                                    time_end        INT NOT NULL,
                                    first_clicked   TINYINT NOT NULL,
                                    second_clicked  TINYINT NOT NULL,
                                    third_clicked   TINYINT NOT NULL,
                                    pause           BIT DEFAULT false,
                                    FOREIGN KEY(game_id) REFERENCES game_table(game_id))""")

        self.curs.execute("""CREATE TABLE IF NOT EXISTS playing_cards_deck_table 
                                (game_id INTEGER NOT NULL,
                                    card_number     INT NOT NULL,
                                    card            varchar(4),
                                    FOREIGN KEY(game_id) REFERENCES game_table(game_id))""")

    @check_func
    def add_player(self, player):
        """ Add a value to the player_tabel
        """
        #Placeholder : insert variables in sqlite3
        self.curs.execute(f"""INSERT INTO player_table(player_id) VALUES (?)""", (player,))
        self.conn.commit()

    @check_func
    def add_game(self, games):
        """ Add a value to the main table and
        """
        #Placeholder : insert variables in sqlite3
        self.curs.execute(f"""INSERT INTO game_table(player_id, total_time, score, wrong, correct) VALUES (?,?,?,?,?)""", games)
        self.conn.commit()

    @check_func
    def add_time(self, items):
        """ Add a value to the main table and
        """
        #Placeholder : insert variables in sqlite3
        self.curs.execute(f"""INSERT INTO time_table(game_id, time_begin, time_end, first_clicked, second_clicked, third_clicked, pause) VALUES (?,?,?,?,?,?,?)""", items)
        self.conn.commit()

    @check_func
    def show_tables(self):
        """ Add a value to the main table and
        """
        print("\nplayer_table")
        self.curs.execute("""SELECT * FROM player_table""")
        for x in self.curs:
            print(x)

        print("\ngame_table")
        self.curs.execute("""SELECT * FROM game_table""")
        for x in self.curs:
            print(x)

        print("\ntime_table")
        self.curs.execute("""SELECT * FROM time_table""")
        for x in self.curs:
            print(x)
        
        print("\nplaying_cards_deck_table")
        self.curs.execute("""SELECT * FROM playing_cards_deck_table""")
        for x in self.curs:
            print(x)

    @check_func
    def add_deck(self, list_data):
        """ Add a values to the deck and
        """
        self.curs.executemany("INSERT INTO playing_cards_deck_table VALUES (?, ?, ?)", list_data)
        self.conn.commit()

    @check_func
    def show_test(self):
        """ Add a value to the main table and
        """
        print("\nJoining tables")
        self.curs.execute("""SELECT
                                pl.player_id,
                                gm.game_id,
                                gm.total_time,
                                tm.time_begin,
                                tm.time_end
                            FROM player_table pl
                            JOIN game_table gm
                            ON  gm.player_id = pl.player_id
                            JOIN time_table tm
                            ON gm.game_id = tm.game_id
                            WHERE pl.player_id = "Frins" OR pl.player_id ="Frans";""")
        for x in self.curs:
            print(x)


    @check_func
    def add_in_secondary(self, login, app, id, lock):
        """Add data to user's table
        """
        self.curs.execute(f"""INSERT INTO {login} VALUES (?, ?, ?)""", ( app,  id, lock))
        self.conn.commit()

    @check_func
    def check_pass(self, user, app):
        """
        Get a password from the database and return it as  string
        """
        infos = self.curs.execute(f"SELECT login, password FROM {user} WHERE application = '{app}'")
        return list(infos)[0]

    @check_func
    def delete_table(self, user):
        """
        Delete account
        """
        try:
            self.curs.execute(f"""DROP TABLE  {user}""")
        except sq.OperationalError:
            return self.err_find

    @check_func
    def delete_entry(self, user, entry):
        """
        Delete an entry from a user's data base
        """
        try:
            self.curs.execute(f"""DELETE FROM  {user} WHERE application = ? """, (entry))
        except sq.OperationalError:
            return self.err_find

    @check_func
    def update_entry(self, user, entry, change):
        """Update the entry of a user's data base
        """
        self.curs.execute(f"""UPDATE {user} SET password = ? WHERE application = ? """, (change, entry))
        self.conn.commit()


    @check_func
    def add_many(self, list_data):
        self.curs.executemany("INSERT INTO main_table VALUES (?, ?)", list_data)
        self.conn.commit()

    @check_func
    def delete_entry(self, table, id_val):
        self.curs.execute(f"""DELETE FROM {table} WHERE id = ?""", (id_val,))
        self.conn.commit()

    @check_func
    def save_query(self):
       """ save a modification after user verification
       """
       self.conn.commit()

    @check_func
    def check_table(self, table='main_table'):
        """print every row of the table
        """
        logins = {}

        for row in self.curs.execute(f"SELECT * FROM {table}"):
            logins[row[0]] = row[1]
        return logins

    @check_func
    def users_list(self):
        logins = []

        for row in self.curs.execute(f"SELECT id FROM main_table "):
            logins.append(row[0])
        return(logins)


    @check_func
    def control_center(self):
        """ For a custom query, more complex than a one liner
        """
        c_command = input("Enter your command : ")
        self.curs.executescript(c_command)
        self.conn.commit()

    @check_func
    def close_app(self):
        self.conn.close()



if __name__ =='__main__':
    # r1 = [("Jack", 217),
    #       ("Ripley", 'USS Sulaco'),
    #       ("Radamanthe", 1234)
    #       ]
    first_test = DataBase()
    # first_test.add_player("Frans")
    # first_test.add_player("Frons")
    # first_test.add_player("Fruns")
    # first_test.add_player("Frins")

    # tGames = ("Frans", 0, 1, 2, 3)
    # first_test.add_game(tGames)
    # tGames = ("Frons", 0, 1, 2, 3)
    # first_test.add_game(tGames)
    # tGames = ("Fruns", 0, 1, 2, 3)
    # first_test.add_game(tGames)
    # tGames = ("Frins", 0, 1, 2, 3)
    # first_test.add_game(tGames)

    # first_test.show_tables()
    
    # prevTime = time.perf_counter_ns()

    # for i in range(0,100):
    #     while time.perf_counter_ns() < (prevTime+5000000):
    #         pass
    #     curTime = time.perf_counter_ns()
    #     tTimes = (1+i%4, prevTime, curTime, 1, 2, 3,False)
    #     first_test.add_time(tTimes)
    #     prevTime = time.perf_counter_ns()

    # first_test.show_test()

    gameIdArray = [1 for a in range(81)]
    cardNumber = [a+1 for a in range(81)]
    cardDeckArray =  [''.join(map(str,[a,b,c,d])) for a in ['1','2','3'] for b in ['1','2','3'] for c in ['1','2','3'] for d in ['1','2','3']]

    
    cards_deck = list(zip(gameIdArray, cardNumber, cardDeckArray))

    first_test.add_deck(cards_deck)
    first_test.show_tables()
    first_test.close_app()


    # first_test.save_query()
    # first_test.add_many(r1)
    # first_test.create_secondary("Jack")
    # first_test.save_query()
    # first_test.add_in_secondary("Jack", "facebook", "jack D", "123" )
    # print(first_test.check_table("Jack"))
    # first_test.update_entry("Jack", 'facebook', 'pass2')
    # print(first_test.check_account)
    # print(first_test.users_list())
    # print(type(first_test.users_list()))
