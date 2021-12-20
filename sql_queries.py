import configparser


"""
THIS FILE LISTS ALL THE QUERIES THAT WILL BE EXECUTED IN THE REDSHIFT CLUSTER. 
IT IS MEANT AS A REFERENCE FILE FOR THE FILES "etl.py" and "create_tables.py"
"""

#######################################################################
# GET AWS CREDENTIALS FROM CONFIG FILE
#######################################################################

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

LOG_DATA = config.get('S3', 'LOG_DATA')
LOG_JSONPATH = config.get('S3', 'LOG_JSONPATH')
SONG_DATA = config.get('S3', 'SONG_DATA')
IAM_ROLE = config.get('IAM_ROLE', 'ARN')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS S_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS S_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS F_songplay;"
user_table_drop = "DROP TABLE IF EXISTS D_user;"
song_table_drop = "DROP TABLE IF EXISTS D_song;"
artist_table_drop = "DROP TABLE IF EXISTS D_artist;"
time_table_drop = "DROP TABLE IF EXISTS D_time;"

# CREATE TABLES

#######################################################################
# CREATE STAGING TABLES
#######################################################################

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS S_events (
    artist VARCHAR sortkey, 
    auth VARCHAR,
    first_name VARCHAR, 
    gender CHAR(1),
    item_in_session INT,
    last_name VARCHAR, 
    length FLOAT, 
    level VARCHAR, 
    location VARCHAR,
    method VARCHAR, 
    page VARCHAR, 
    registration BIGINT, 
    session_id VARCHAR, 
    song VARCHAR,
    status INT, 
    ts BIGINT,
    user_agent VARCHAR, 
    user_id INT);
""")



staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS S_songs (
    artist_id VARCHAR,
    artist_latitude FLOAT,
    artist_location TEXT,
    artist_longitude FLOAT,
    artist_name VARCHAR sortkey,
    duration FLOAT,
    num_songs INT,
    song_id VARCHAR,
    title VARCHAR,
    year INT) ; 
    """)

#######################################################################
# CREATE FACT AND DIMENSION TABLES
#######################################################################

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS F_songplay (
    songplay_id INTEGER IDENTITY(0,1) PRIMARY KEY sortkey,
    start_time timestamp, 
    user_id int, 
    level varchar,
    song_id varchar, 
    artist_id varchar, 
    session_id varchar,
    location varchar, 
    user_agent varchar) ; 
    """)

user_table_create = ("""CREATE TABLE IF NOT EXISTS D_user (
    user_id int PRIMARY KEY, 
    first_name varchar, 
    last_name varchar,
    gender varchar, 
    level varchar); 
    """)

song_table_create = ("""CREATE TABLE IF NOT EXISTS D_song (
    song_id varchar PRIMARY KEY, 
    title varchar,
    artist_id varchar, 
    year int, 
    duration numeric); 
    """)

artist_table_create = ("""CREATE TABLE IF NOT EXISTS D_artist (
    artist_id varchar PRIMARY KEY,
    name varchar, 
    location varchar, 
    latitude varchar,
    longitude varchar) ; 
    """)

time_table_create = ("""CREATE TABLE IF NOT EXISTS D_time (
    time_key INTEGER IDENTITY(0,1) PRIMARY KEY sortkey, 
    start_time time,
    hour int,
    day int, 
    week int,
    month int, 
    year int,
    weekday int); 
    """)

#######################################################################
# COPY EVENTS LOG DATA INTO STAGING_EVENTS TABLE FROM AWS S3 BUCKET
#######################################################################

staging_events_copy = ("""COPY S_events 
                       FROM {} 
                       iam_role {}
                       json {}
                       """).format(LOG_DATA,IAM_ROLE,LOG_JSONPATH)

staging_songs_copy = (""" COPY S_songs 
                      FROM {}
                      iam_role {}
                      json 'auto'                  
                      """).format(SONG_DATA,IAM_ROLE)



#######################################################################
# INSERT INTO FACT AND DIMENSION TABLES
#######################################################################

songplay_table_insert = ("""INSERT INTO F_songplay (start_time,user_id,level,song_id,artist_id,session_id, location, user_agent)
SELECT timestamp 'epoch' + se.ts/1000 * interval '1 second' as start_time,
       se.user_id, 
       se.level,
       ss.song_id,
       ss.artist_id,
       se.session_id,
       se.location, 
       se.user_agent
    FROM S_events se 
    JOIN S_songs ss ON se.artist = ss.artist_name AND se.song=ss.title
    WHERE se.page='NextSong';
    """)
                                                                                                                                  
user_table_insert = ("""INSERT INTO D_user (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT user_id, first_name,last_name,gender,level
    FROM S_events 
    WHERE page='NextSong';
    """)

song_table_insert = ("""INSERT INTO D_song (song_id, title, artist_id, year, duration)
    SELECT song_id, title, artist_id, year, duration
    FROM S_songs
    WHERE song_id IS NOT NULL; 
""")

artist_table_insert = ("""INSERT INTO D_artist (artist_id,name, location, latitude, longitude)
    SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
    FROM S_songs
    WHERE artist_id IS NOT NULL; 
""")


time_table_insert = ("""INSERT INTO D_time (start_time,hour,day, week, month,year, weekday) 
     SELECT start_time,
            extract(hour FROM start_time),
            extract(day FROM start_time),
            extract(week FROM start_time),
            extract(month FROM start_time),
            extract(year FROM start_time),
            extract(dayofweek FROM start_time)
     FROM F_songplay; 
    """)


# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
