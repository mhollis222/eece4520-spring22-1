import mysql.connector
import json
import Model.move


class Database:

    _instance = None

    def __new__(cls, host, user, password):
        """
        initializes singleton database manager object
        :param host: server host, to remain localhost for purposes of project
        :param user: username for server login, ensure user has DB mgmt privileges
        :param password: password for server login corresponding to username
        :return: new instance or original instance if created already
        """
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._config = {
                'host': host,
                'user': user,
                'password': password,
            }
            cls._instance._connection = cls._instance._connect()
            cls._instance._cursor = cls._instance._connection.cursor()
            cls._instance._init_db()
            cls._instance._init_table()
        return cls._instance

    def _connect(self):
        """
        establish connection to mySQL database from parameters enumerated during instantiation
        :return: mySQL database connection
        """
        try:
            cnx = mysql.connector.connect(**self._get_config())
        except mysql.connector.Error as err:
            print("mySQL connection failed: ", err)
            return exit()
        return cnx

    def _get_config(self):
        """
        getter for server configuration information
        :return: server config details
        """
        return self._config

    def _init_db(self):
        """
        initialize database within mySQL server if not already created, select database for future SQL commands
        :return: none
        """
        try:
            self._cursor.execute("CREATE DATABASE IF NOT EXISTS reversi")
        except mysql.connector.DatabaseError as err:
            print("Failed to create database: ", err)
            return exit()
        self._cursor.execute("USE reversi")

    def fetch_user_data(self):
        self._cursor.execute("SELECT * FROM users")
        data = self._cursor.fetchall()
        entry_list = list()

        for elem in data:
            entry = {"username": elem[0],
                     "password": elem[1],
                     "elo": elem[2],
                     "high_score": elem[3],
                     "wins": elem[4],
                     "losses": elem[5]}
            entry_list.append(entry)
        return entry_list

    def fetch_game_data(self, game_id: int):
        self._cursor.execute("SELECT * FROM games WHERE gameid = (%s)", [game_id])
        elem = self._cursor.fetchone()
        game = {"gameid": elem[0],
                "lastactiveplayer": elem[1],
                "gamestate": (json.dumps(elem[2][0]), json.dumps(elem[2][1]))}
        return game

    def _init_table(self):
        """
        initialize table of users within database if not created already
        :return: none
        """
        print("tables initializing")
        try:
            self._cursor.execute(
                "CREATE TABLE IF NOT EXISTS users("
                " username varchar(20) NOT NULL,"
                " password varchar(20) NOT NULL,"
                " elo int NOT NULL,"
                " highscore int NOT NULL,"
                " wins int NOT NULL,"
                " losses int NOT NULL);"
            )
            self._cursor.execute(
                "CREATE TABLE IF NOT EXISTS games("
                " gameid int NOT NULL,"
                " lastactiveplayer varchar(20),"
                " gamestate JSON);"
            )
        except mysql.connector.ProgrammingError as err:
            print("Failed to create table: ", err)
            exit()

    def write_user(self, username, password):
        """
        check table of current users and add new user to table if not existent already, or otherwise corresponding to
        a reserved string
        :param username: username to register
        :param password: password to register
        :return: none
        """
        self._cursor.execute("SELECT username FROM users")
        try:
            users = self._cursor.fetchall()
            # realistically this line should be: `if username in users or username in ['AI', 'local', 'guest']:`
            for user in users:
                if user[0] == username:  # prevents users from making duplicate usernames
                    return -1
                if user[0] == 'AI':  # prevents users from signing up as unique AI tag
                    return -1
                if user[0] == 'local':  # prevents users from signing up as unique local tag
                    return -1
                if user[0] == 'guest':  # prevents users from signing up as unique guest tag
                    return -1
        except mysql.connector.errors as err:
            print("Failed to fetch active users in database: ", err)
            pass
        add_elements = (
            "INSERT INTO users (username, password, elo, highscore, wins, losses) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        self._cursor.execute(add_elements, (username, password, 1500, 0, 0, 0))
        return 1

    def write_update_turn(self, game_id: int, last_player, last_move: Model.move.Move):
        """
        update game state in game instance table
        :param PRIMARY KEY game_id: game to update state information
        :param last_player: last active player (to determine turn order on restore)
        :param last_move: turn data to track - appended to JSON list
        :return: none
        """
        update_elements = (
            "UPDATE games "
            "SET lastactiveplayer = (%s), gamestate = JSON_ARRAY_APPEND(gamestate, '$', (%s)), "
            "gamestate = JSON_ARRAY_APPEND(gamestate, '$[last]', (%s)), gameid = (%s)"
        )
        self._cursor.execute(update_elements, (last_player, last_move.get_coords()[0], last_move.get_coords()[1],
                                               game_id))

    def write_update_game_complete(self, game_id):
        """
        remove game instance from database
        :param game_id: game to be removed from database
        :return: none
        """
        self._cursor.execute("DELETE FROM games WHERE gameid = (%s)", [game_id])

    def write_update_users_complete(self, winner, winner_elo, winner_hs, loser, loser_elo, loser_hs):
        """
        update user data for online multiplayer game, including high score and ELO
        :param winner: PRIMARY KEY user whose data will be updated based on game completion
        :param winner_elo: ELO rating corresponding to user
        :param winner_hs: score to be compared versus user high score and potentially update
        :param loser: PRIMARY KEY user whose data will be updated based on game completion
        :param loser_elo: ELO rating corresponding to user
        :param loser_hs: score to be compared versus user high score and potentially update
        :return: none
        """
        self._cursor.execute("SELECT * FROM users WHERE username = (%s)", [winner])
        winner_hs_og = self._cursor.fetchone()
        if winner_hs < winner_hs_og[3]:
            winner_hs = winner_hs_og[3]
        self._cursor.execute("SELECT * FROM users WHERE username = (%s)", [loser])
        loser_hs_og = self._cursor.fetchone()
        if loser_hs < winner_hs_og[3]:
            loser_hs = loser_hs_og[3]
        update_winner = (
            "UPDATE users "
            "SET elo = (%s), highscore = (%s), wins = wins + 1 "
            "WHERE username = (%s)"
        )
        update_loser = (
            "UPDATE users "
            "SET elo = (%s), highscore = (%s), losses = losses + 1 "
            "WHERE username = (%s)"
        )
        self._cursor.execute(update_winner, (winner_elo, winner_hs, winner))
        self._cursor.execute(update_loser, (loser_elo, loser_hs, loser))

    def write_update_game_start(self):
        """
        add game instance to database with game ID
        :return: id_max
        """
        update_elements = (
            "INSERT INTO games (gameid, lastactiveplayer, gamestate) "
            "VALUES (%s, NULL, JSON_ARRAY())"
        )
        self._cursor.execute("SELECT * FROM games")
        data = self._cursor.fetchall()
        id_max = 0
        for row in data:
            if row[0] > id_max:
                id_max = row[0]
        id_max = id_max + 1
        self._cursor.execute(update_elements, [id_max])
        return id_max

    def _clear_data(self):
        """
        clear all user data stored in database
        :return: none
        """
        self._cursor.execute("DROP TABLE IF EXISTS users;")
        self._cursor.execute("DROP TABLE IF EXISTS games;")

    def verify_credentials(self, username, password):
        """
        confirm entered user credentials are valid and that username/password match for that entry in user table
        :param username: username selected for login
        :param password: password selected for login, to correspond to entered username
        :return: valid? (boolean)
        """
        for element in self.fetch_user_data():
            if element.get("username") == username:
                if element.get("password") == password:
                    return True
                else:
                    return False
        return False

    def sorted_leaderboard(self):
        """
        return user dictionary entry list sorted by ELO rating
        :return: sorted user data list
        """
        def by_elo(e: dict):
            return e.get("elo")
        leaderboard = self.fetch_user_data()
        leaderboard.sort(key=by_elo)
        return leaderboard

    @staticmethod
    def test_db():
        """
        comprehensive test method for verifying functionality of operations within Database class
        :return: none
        """
        # connection details
        ipaddr = 'localhost'
        db_user = 'reversi'
        db_password = 'eece4520'

        # initialization of db object, passing above as arguments
        db = Database(ipaddr, db_user, db_password)

        db._clear_data()  # use only for testing db
        db._init_table()

        # initialization of table
        print("EMPTY DB")
        print(db.fetch_user_data())

        # sample values for signup
        signup_username = "test"
        signup_password = "4520"

        # create new user and test login
        db.write_user(signup_username, signup_password)
        db.write_user("opp", "xxx")
        print("USER ADDED")
        print(db.fetch_user_data())

        # login
        username = input("Username: ")
        password = input("Password: ")
        if db.verify_credentials(username, password):
            print("Login successful")
        else:
            print("Invalid credentials")
            exit()

        # sample values for game completion
        win_elo = 1600
        lose_elo = 1400
        win_high_score = 15
        lose_high_score = 14

        # start game (called when game is initialized)
        game_id = db.write_update_game_start()
        print("GAME STARTED")
        print(db.fetch_game_data(game_id))

        # update game state (called every time turn resolves)
        # game state is a double that represents game state
        db.write_update_turn(game_id, username, Model.move.Move(4, 5))
        print("TURN UPDATED")
        print(db.fetch_game_data(game_id))

        # update elo and score when game finishes (called when game is completed)
        db.write_update_game_complete(game_id)
        db.write_update_users_complete(username, win_elo, win_high_score, "opp", lose_elo, lose_high_score)
        print("GAME FINISHED")
        print(db.fetch_user_data())
        # print(db.fetch_game_data(game_id))

        # leaderboard test
        db.write_user("user1", "pass1")
        db.write_user("user2", "pass2")
        db.write_update_users_complete("user1", 1700, 20, "user2", 1800, 25)
        db.write_user("user3", "pass3")
        db.write_user("user4", "pass4")
        db.write_update_users_complete("user3", 1300, 5, "user4", 1900, 30)
        print("LEADERBOARD SORTED BY DATE ADDED")
        print(db.fetch_user_data())
        print("LEADERBOARD SORTED BY ELO")
        print(db.sorted_leaderboard())

        # close db
        db._connection.close()

        print("\nAll operations completed successfully")
