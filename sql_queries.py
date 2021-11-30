import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS S_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS S_songs"
songplay_table_drop = "DROP TABLE IF EXISTS F_songplay;"
user_table_drop = "DROP TABLE IF EXISTS D_user;"
song_table_drop = "DROP TABLE IF EXISTS D_song;"
artist_table_drop = "DROP TABLE IF EXISTS D_artist;"
time_table_drop = "DROP TABLE IF EXISTS D_time;"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS S_events (
    artist VARCHAR, 
    auth VARCHAR,
    firstName VARCHAR, 
    gender VARCHAR,
    itemInSession INT,
    lastName VARCHAR, 
    length VARCHAR, 
    level VARCHAR, 
    location VARCHAR,
    method VARCHAR, 
    page VARCHAR, 
    registration BIGINT, 
    sessionId VARCHAR, 
    song VARCHAR,
    status INT, 
    ts BIGINT,
    userAgent VARCHAR, 
    userId INT
);

""")

staging_songs_table_create = ("""
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS F_songplay (songplay_id INTEGER IDENTIRY(0,1) PRIMARY KEY sortkey,
                                       user_id int, 
                                       level varchar,
                                       song_id varchar, 
                                       artist_id varchar, 
                                       session_id varchar,
                                       location varchar, 
                                       useragent varchar,
                                       
                        CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES D_user(user_id),\
                        CONSTRAINT fk_song FOREIGN KEY (song_id) REFERENCES D_song(song_id),\
                        CONSTRAINT fk_artist FOREIGN KEY (artist_id) REFERENCES D_artist(artist_id));""")

user_table_create = "CREATE TABLE IF NOT EXISTS D_user(user_id int PRIMARY KEY, first_name varchar, last_name varchar,gender varchar, level varchar); "

song_table_create = "CREATE TABLE IF NOT EXISTS D_song(song_id varchar PRIMARY KEY, title varchar, artist_id varchar, year int, duration numeric) ;  "

artist_table_create = "CREATE TABLE IF NOT EXISTS D_artist(artist_id varchar PRIMARY KEY, name varchar, location varchar, latitude varchar, longitude varchar) ; "

time_table_create = "CREATE TABLE IF NOT EXISTS D_time(time_key serial PRIMARY KEY, start_time time, hour int, day int, week int, month int, year int, weekday int)   ;"

# STAGING TABLES

staging_events_copy = ("""COPY staging_events 
                       FROM {} 
                       iam_role {}
                       json {}
                       """).format(config.get('S3','LOG_DATA'),config.get('IAM_ROLE','ARN'),config.get('S3','LOG_JSONPATH'))

staging_songs_copy = (""" COPY staging_songs 
                      FROM {}
                      iam_role {}
                      json 
                      
                      """).format()



# FINAL TABLES

songplay_table_insert = """INSERT INTO F_songplay (start_time, user_id, level, song_id, artist_id, session_id, location, useragent) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"""
                                                                    
                                                                     

user_table_insert = "INSERT INTO D_user (user_id, first_name, last_name, gender, level) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (user_id) DO UPDATE SET level=EXCLUDED.level;"

song_table_insert = "INSERT INTO D_song (song_id, title, artist_id, year, duration) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING;" 

artist_table_insert = "INSERT INTO D_artist (artist_id, name, location, latitude, longitude) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING;"


time_table_insert = "INSERT INTO D_time (start_time, hour, day, week, month, year, weekday) VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING;"


# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
