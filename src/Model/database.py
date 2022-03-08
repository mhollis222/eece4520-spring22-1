import mysql.connector


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

    def fetch_data(self):
        """
        fetch users table from database and transform raw data into list of dictionary entries for each row/user
        :return: list of user dictionary entries
        """
        self._cursor.execute("SELECT * FROM users")
        data = self._cursor.fetchall()
        entry_list = list()

        for elem in data:
            entry = {"username": elem[0],
                     "password": elem[1],
                     "elo": elem[2],
                     "high_score": elem[3],
                     "opponent": elem[4],
                     "active_turn": elem[5]}
            entry_list.append(entry)
        return entry_list

    def _init_table(self):
        """
        initialize table of users within database if not created already
        :return: none
        """
        try:
            self._cursor.execute(
                "CREATE TABLE IF NOT EXISTS users("
                " username varchar(20) NOT NULL,"
                " password varchar(20) NOT NULL,"
                " elo int NOT NULL,"
                " highscore int NOT NULL,"
                " opponent varchar(20) NOT NULL,"
                " activeturn double NOT NULL);"
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
            "INSERT INTO users (username, password, elo, highscore, opponent, activeturn) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        self._cursor.execute(add_elements, (username, password, 1500, 0, '', 0))

    def write_update_turn(self, user, turn):
        """
        update turn attribute in user table to track game state
        TODO: migrate to new table in database
        :param PRIMARY KEY user: user whose turn is tracked
        :param turn: turn data to track - format and datatype for state tracking TBD
        :return: none
        """
        update_elements = (
            "UPDATE users "
            "SET activeturn = (%s) "
            "WHERE username = (%s)"
        )
        self._cursor.execute(update_elements, (turn, user))

    def write_update_game_complete(self, user, elo, score):
        """
        update user data for online multiplayer game, including high score and ELO
        TODO: split method for new table in database
        :param user: PRIMARY KEY user whose data will be updated based on game completion
        :param elo: ELO rating corresponding to user
        :param score: score to be compared versus user high score and potentially update
        :return: none
        """
        update_elements = (
            "UPDATE users "
            "SET elo = (%s), highscore = (%s), opponent = (%s) "
            "WHERE username = (%s)"
        )
        self._cursor.execute(update_elements, (elo, score, '', user))

    def write_update_game_start(self, user, opponent):
        """
        update user's opponent for ongoing match beginning
        TODO: migrate to new table in database
        :param user: PRIMARY KEY user whose match status is being tracked
        :param opponent: username or preset string corresponding to player user is engaged in a game with
        :return: none
        """
        update_elements = (
            "UPDATE users "
            "SET opponent = (%s) "
            "WHERE username = (%s)"
        )
        self._cursor.execute(update_elements, (opponent, user))

    def _clear_data(self):
        """
        clear all user data stored in database
        :return: none
        """
        self._cursor.execute("DROP TABLE IF EXISTS users;")

    def verify_credentials(self, username, password):
        """
        confirm entered user credentials are valid and that username/password match for that entry in user table
        :param username: username selected for login
        :param password: password selected for login, to correspond to entered username
        :return: valid? (boolean)
        """
        for element in self.fetch_data():
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
        leaderboard = self.fetch_data()
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

        # initialization of table
        print("EMPTY DB")
        print(db.fetch_data())

        # sample values for signup
        signup_username = "test"
        signup_password = "4520"

        # create new user and test login
        db.write_user(signup_username, signup_password)
        print("USER ADDED")
        print(db.fetch_data())

        # login
        username = input("Username: ")
        password = input("Password: ")
        if db.verify_credentials(username, password):
            print("Login successful")
        else:
            print("Invalid credentials")
            exit()

        # sample values for game start
        # note: opponent should be 'AI' or 'local' if not playing online
        opponent = 'sample_opponent'

        # sample values for game completion
        new_elo = 1600
        new_high_score = 15

        # sample values for game state
        active_turn = 0xA5E3

        # start game (called when game is initialized)
        db.write_update_game_start(username, opponent)
        print("GAME STARTED")
        print(db.fetch_data())

        # update game state (called every time turn resolves)
        # game state is a double that represents game state
        # TODO: method in model for parsing game state from this double
        db.write_update_turn(username, active_turn)
        print("TURN UPDATED")
        print(db.fetch_data())

        # update elo and score when game finishes (called when game is completed)
        db.write_update_game_complete(username, new_elo, new_high_score)
        print("GAME FINISHED")
        print(db.fetch_data())

        # leaderboard test
        db.write_user("user1", "pass1")
        db.write_update_game_complete("user1", 1700, 20)
        db.write_user("user2", "pass2")
        db.write_update_game_complete("user2", 1800, 25)
        db.write_user("user3", "pass3")
        db.write_update_game_complete("user3", 1300, 5)
        print("LEADERBOARD SORTED BY DATE ADDED")
        print(db.fetch_data())
        print("LEADERBOARD SORTED BY ELO")
        print(db.sorted_leaderboard())

        # close db
        db._connection.close()

        print("\nAll operations completed successfully")
