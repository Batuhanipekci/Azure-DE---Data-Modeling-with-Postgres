# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE songplays (
    songplay_id SERIAL PRIMARY KEY, 
    start_time BIGINT NOT NULL, 
    user_id VARCHAR(8) NOT NULL, 
    level VARCHAR(8) NOT NULL, 
    song_id VARCHAR(18) NOT NULL, 
    artist_id VARCHAR(18), 
    session_id INT , 
    location VARCHAR(128), 
    user_agent VARCHAR(512)
);
""")

user_table_create = ("""
CREATE TABLE users (
    user_id INT PRIMARY KEY, 
    first_name VARCHAR(16), 
    last_name VARCHAR(16), 
    gender VARCHAR(1), 
    level VARCHAR(8) NOT NULL
    )
;
""")

song_table_create = ("""
CREATE TABLE songs (
    song_id VARCHAR(18) PRIMARY KEY, 
    title VARCHAR(128), 
    artist_id VARCHAR(18), 
    year INT, 
    duration NUMERIC(10,5)
    )
;
""")

artist_table_create = ("""
CREATE TABLE artists (
    artist_id VARCHAR(18) PRIMARY KEY, 
    name VARCHAR(128), 
    location VARCHAR(128), 
    latitude NUMERIC(10,5), 
    longitude NUMERIC(10,5)
    )
;
""")

time_table_create = ("""\
CREATE TABLE time (
    start_time BIGINT PRIMARY KEY, 
    hour INT NOT NULL, 
    day INT NOT NULL,
    week INT NOT NULL, 
    month INT NOT NULL, 
    year INT NOT NULL, 
    weekday VARCHAR(18) NOT NULL
    )
;
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (
    start_time,
    user_id,
    level,
    song_id,
    artist_id,
    session_id,
    location,
    user_agent
    ) SELECT 
        t.start_time,
        u.user_id,
        u.level,
        s.song_id,
        a.artist_id,
        %s,
        %s,
        %s
    FROM songs AS s
    LEFT JOIN artists AS a
    ON s.artist_id = a.artist_id
    LEFT JOIN users AS u
    ON u.user_id = %s
    LEFT JOIN time AS t
    ON t.start_time = %s
    WHERE s.song_id = %s
    AND a.artist_id = %s
;
""")

user_table_insert = ("""
INSERT INTO users (
    user_id,
    first_name,
    last_name,
    gender,
    level
         ) VALUES (
        %s, %s, %s, %s, %s
        )
    ON CONFLICT DO NOTHING
;
""")

song_table_insert = ("""
INSERT INTO songs (
    song_id,
    title,
    artist_id,
    year,
    duration
    ) VALUES (
        %s, %s, %s, %s, %s
    )
    ON CONFLICT DO NOTHING;
""")

artist_table_insert = ("""
INSERT INTO artists (
    artist_id,
    name,
    location,
    latitude,
    longitude
         ) VALUES (
        %s, %s, %s, %s, %s
        )
    ON CONFLICT DO NOTHING
;
""")


time_table_insert = ("""
INSERT INTO time (
   start_time,
   hour,
   day,
   week,
   month,
   year,
   weekday
         ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s
        )
    ON CONFLICT DO NOTHING
;
""")

# FIND SONGS

song_select = ("""
SELECT s.song_id, a.artist_id FROM songs AS s
LEFT JOIN artists as a
ON s.artist_id = a.artist_id
WHERE s.title = %s
AND a.name = %s
AND s.duration = %s
;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]