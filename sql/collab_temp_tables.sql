/* 
The following query is written to work in a SQLite database, specifically through the sqlite3 Python module.
Depending on SQL dialect and database engine, this query may need to be modified.
*/

-- Temp table of total amounts of unique writers/producers/artists per era
-- Used in section "Most Collaborative Eras - Unique collaborators Per Era"
DROP 
    TABLE IF EXISTS temp.unique_credits_per_era;
CREATE TABLE temp.unique_credits_per_era (
    era TEXT,
    unique_writers INTEGER,
    unique_producers INTEGER,
    unique_artists INTEGER
);
INSERT INTO temp.unique_credits_per_era 
SELECT 
    a.category AS era,
    COUNT(DISTINCT w.song_writer) as unique_writers,
    COUNT(DISTINCT p.song_producer) as unique_producers,
    COUNT(DISTINCT sa.song_artist) as unique_artists
FROM 
    albums a
    LEFT JOIN songs s ON a.album_title = s.album_title
    LEFT JOIN writers w ON s.song_title = w.song_title
    LEFT JOIN producers p ON s.song_title = p.song_title
    LEFT JOIN artists sa ON s.song_title = sa.song_title
GROUP BY
    a.category;

-- Temp table of total number of credits (writers, producers, artists) per song
-- Used in section "Most Collaborative Eras - Average collaborators Per Song By Era"
DROP 
    TABLE IF EXISTS temp.credit_counts_per_song;
CREATE TABLE temp.credit_counts_per_song (
    album_title TEXT,
    song_title TEXT,
    writers INTEGER,
    producers INTEGER,
    artists INTEGER
);
INSERT INTO temp.credit_counts_per_song
SELECT
    s.album_title AS album_title,
    s.song_title AS song_title,
    COUNT(DISTINCT w.song_writer) AS writers,
    COUNT(DISTINCT p.song_producer) AS producers,
    COUNT(DISTINCT sa.song_artist) AS artists
FROM
    songs s
    JOIN writers w ON s.song_title = w.song_title
    JOIN producers p ON s.song_title = p.song_title
    JOIN artists sa ON s.song_title = sa.song_title
GROUP BY
    s.song_title;

-- Temp table of total songs and total number of credits (writers, producers, artists) per era
-- Used in section "Most Collaborative Eras - Average Musicians Per Song By Era"
DROP 
    TABLE IF EXISTS temp.credit_counts_per_era;
CREATE TABLE temp.credit_counts_per_era (
    era TEXT,
    total_songs INTEGER,
    total_writers INTEGER,
    total_producers INTEGER,
    total_artists INTEGER
);
INSERT INTO temp.credit_counts_per_era
SELECT
    a.category AS era,
    COUNT(DISTINCT song_title) AS total_songs,
    SUM(cc.writers) AS total_writers,
    SUM(cc.producers) AS total_producers,
    SUM(cc.artists) AS total_artists
FROM
    credit_counts_per_song cc
    JOIN albums a ON cc.album_title = a.album_title
GROUP BY
    a.category;

-- Temp table of collaborators and the songs they worked on, regardless of contribution
-- Used in section "Frequent Collaborators"
DROP 
    TABLE IF EXISTS temp.collaborators_per_song;
CREATE TABLE temp.collaborators_per_song (
    era TEXT,
    song_title TEXT,
    collaborator TEXT,
    songs_worked_on INTEGER
);
INSERT INTO temp.collaborators_per_song
WITH collaborators as (
    SELECT 
        a.category AS era,
        s.song_title as song_title,
        w.song_writer AS collaborator
    FROM 
        albums a
        JOIN songs s ON a.album_title = s.album_title
        JOIN writers w ON s.song_title = w.song_title
    UNION ALL
    SELECT 
        a.category AS era,
        s.song_title as song_title,
        p.song_producer AS collaborator
    FROM 
        albums a
        JOIN songs s ON a.album_title = s.album_title
        JOIN producers p ON s.song_title = p.song_title
    UNION ALL
    SELECT 
        a.category AS era,
        s.song_title as song_title,
        sa.song_artist AS collaborator
    FROM 
        albums a
        JOIN songs s ON a.album_title = s.album_title
        JOIN artists sa ON s.song_title = sa.song_title
    ORDER BY
        a.category, s.song_title
)
SELECT
    era,
    song_title,
    collaborator,
    1 AS songs_worked_on
FROM
    collaborators
GROUP BY
    era, song_title, collaborator;

-- Temp table of collaborators and their totals songs worked on per era, removing Taylor Swift
-- Used in section "Frequent Collaborators"
DROP 
    TABLE IF EXISTS temp.collaborators_per_era;
CREATE TABLE temp.collaborators_per_era (
    era TEXT,
    collaborator TEXT,
    songs INTEGER,
    total_songs INTEGER
);
INSERT INTO temp.collaborators_per_era
SELECT
    era,
    collaborator,
    SUM(songs_worked_on) AS songs,
    SUM(COUNT(*)) OVER (PARTITION BY collaborator) AS total_songs
FROM
    collaborators_per_song
WHERE
    collaborator != 'Taylor Swift'
GROUP BY
    era, collaborator