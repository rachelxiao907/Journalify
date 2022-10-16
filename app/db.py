import sqlite3
import train
import api
from datetime import datetime

DB_FILE = "database.db"
db = sqlite3.connect(DB_FILE)
cur = db.cursor()

cur.execute("""
	CREATE TABLE IF NOT EXISTS users(
	  id INTEGER PRIMARY KEY,
	  username TEXT,
	  password TEXT)""")

cur.execute("""
	CREATE TABLE IF NOT EXISTS entries(
	  user_id INTEGER,
      date TEXT,
	  summary TEXT,
      song TEXT,
      title TEXT,
      image TEXT)""")

db.commit()
db.close()

#####################
#                   #
# Utility Functions #
#                   #
#####################


def register_user(username, password):
	"""
	Tries to add the given username and password into the database.
	Returns False if the user already exists, True if it successfully added the user.
	"""
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()

	c.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(?)", (username,))
	row = c.fetchone()

	if row is not None:
		return False

	c.execute("""INSERT INTO users(username,password) VALUES(?, ?)""",(username,password))
	db.commit()
	db.close()
	return True


def fetch_user_id(username, password):
	"""
	Gets the id of the user with the given username/password combination from the database.
	Returns None if the combination is incorrect.
	"""
	db = sqlite3.connect(DB_FILE)

	# The following line turns the tuple into a single value (sqlite3 commands always return a tuple, even when it is one value)
	# You can read more about row_factory in the official docs:
	# https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
	db.row_factory = lambda curr, row: row[0]
	c = db.cursor()

	c.execute("""
		SELECT id
		FROM   users
		WHERE  LOWER(username) = LOWER(?)
		AND    password = ?
	""", (username, password))

	# user_id is None if no matches were found
	user_id = c.fetchone()

	db.close()

	return user_id


def fetch_username(user_id):
	"""
	Returns the username of the user with the given id.
	"""
	db = sqlite3.connect(DB_FILE)
	db.row_factory = lambda curr, row: row[0]
	c = db.cursor()

	c.execute("SELECT username FROM users WHERE id = ?", (user_id,))
	username = c.fetchone()

	db.close()
	return username


def add_to_journal(user_id, entry, date):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    def is_in_journal(user_id, date):
        c.execute("""
            SELECT *
                FROM   entries
                WHERE  user_id = ?
                AND  date = ?""", (user_id, date))
        summary = c.fetchone()
        return summary is not None # returns True if the summary exists

    if is_in_journal(user_id, date):
        return False #don't add to journal if the entry for that date was already made

    # TODO: ADD SPOTIFY SONG AND IMAGE INTO THE TABLE
    emotion = train.classify(entry)
    song_dict = api.pick_song(emotion)
    print(emotion)
    c.execute("""
        INSERT INTO entries(user_id, date, summary, song, title, image)
            VALUES (?,?,?,?, ?, ?)""", (user_id, date, entry, song_dict['link'], song_dict['title'], song_dict['cover']))
    db.commit()
    db.close()
    print(song_dict['cover'])
    return True # successfully added to library


def fetch_journal(user_id):
    """
    Returns a list of dictionaries of entries which makes up the user's journal
    """
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    c.execute("""
        SELECT date
                , summary
                , song
                , title
                , image 
        FROM   entries
        WHERE  user_id = ? """, (user_id,))
        
    journal = c.fetchall()
    
    entries = []
    for date, summary, song, title, image in journal:
        dict = {
            'date': date,
            'summary': summary,
            'song': song,
            'title': title,
            'image': image
        }
        entries.append(dict)
    
    db.commit()
    db.close()

    format_data = "%B %d, %Y"
    return sorted(entries, key=lambda x: datetime.strptime(x['date'], format_data)) #sort entries by date