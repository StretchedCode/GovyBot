import psycopg2, config

try:
    testDB = psycopg2.connect(database=config.DATABASE, user=config.DB_USER)
    testDB.autocommit = True
except:
    print('failed connection')

def create_table(guild_name: str, usernames):

    testCursor = testDB.cursor()

    testCursor.execute(f"""CREATE TABLE {guild_name} (
                       id BIGSERIAL NOT NULL PRIMARY KEY,
                       user_name VARCHAR(60) NOT NULL,
                       favourite_manga VARCHAR(60)[] DEFAULT '{'{'}{'}'}'
    )""")
    testCursor.close()

    initialInsert(guild_name=guild_name, usernames=usernames)

def initialInsert(guild_name: str, usernames):

    testCursor = testDB.cursor()

    for user in usernames:
        testCursor.execute(f"""INSERT INTO {guild_name} (
                           user_name
        )VALUES('{user.name}')
""")
    testCursor.close()

def insert(user: str, manga: str, guildname:str):

    testCursor = testDB.cursor()
    testCursor.execute(f""" UPDATE {guildname} SET favourite_manga = array_append(favourite_manga, '{manga}') WHERE user_name = '{user}' AND '{manga}' <> ALL (favourite_manga)
""")
    testCursor.close()

def remove(user: str, manga: str, guildname:str):

    testCursor = testDB.cursor()
    testCursor.execute(f""" UPDATE {guildname} SET favourite_manga = array_remove(favourite_manga, '{manga}') WHERE user_name = '{user}'
""")
    testCursor.close()


def fetchList(user: str, guildname: str):
    testCursor = testDB.cursor()

    testCursor.execute(f"""SELECT unnest(favourite_manga) FROM convicts WHERE user_name = '{user}' GROUP BY user_name, favourite_manga""")
    
    data = testCursor.fetchall()
    testCursor.close()
    print(data)

    return data


def fetchPopular(guildname: str):
    testCursor = testDB.cursor()

    testCursor.execute(f"""SELECT unnest(favourite_manga), count(*) FROM {guildname} GROUP BY unnest(favourite_manga) ORDER BY count(*) DESC;
""")

    data = testCursor.fetchall()

    return data

"""

Queries to be implemented

SELECT unnest(favourite_manga), count(*) FROM convicts GROUP BY unnest(favourite_manga) ORDER BY count(*) DESC;

SELECT user_name, unnest(favourite_manga) FROM convicts WHERE user_name = 'stretched.' GROUP BY user_name, favourite_manga;

"""