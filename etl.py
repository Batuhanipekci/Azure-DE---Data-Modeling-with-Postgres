import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    - Reads the song file given a filepath
    - Takes subsets of the data for songs and artists tables
    - Loads data into songs and artists tables by executing relevant sql scripts 
    """
    # open song file
    df =  pd.read_json(filepath, typ='series')

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data =  df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    - Reads the log file given a filepath
    - Filters the data by page column equals to NextSong
    - Extracting date features by converting timestamp column to datetime object
    - Loads data into time and users tables by executing relevant sql scripts
    - Executes the song_select script to find songs and artists that are matching to the data
    - Populates the songplays table iterately given the relevant sql script
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = (df['ts'], t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ('timestamp', 'hour', 'day', 'weekofyear', 'month', 'year', 'weekday')
    time_df = pd.concat(time_data, axis=1)
    time_df.columns = column_labels

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None
        
        # insert songplay record
        songplay_data = (row.sessionId, row.location, row.userAgent, row.userId, row.ts, songid, artistid)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    - Collects all json files in all subdirectories given a filepath
    - Calculates the number of files for logging purposes
    - Executes a given function func iterating on the json file
    - Commits results to the database iteratively
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Establishes connection to the local databasea and runs process_data for song and log data
    Closes the database connection after the data pipeline is completed.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    print("Song data has been loaded successfully")
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)
    print("Log data has been loaded successfully")

    conn.close()


if __name__ == "__main__":
    main()