import sqlalchemy
from pprint import pprint
engine = sqlalchemy.create_engine('postgresql://postgres:gabs@localhost:5432/home3')
connection = engine.connect()


# 1 Количество исполнителей в каждом жанре
select_1 = connection.execute("""
    SELECT name_genre,COUNT(genre_musicains.musician_id) FROM musicians
    JOIN genre_musicains ON musicians.id = genre_musicains.musician_id
    JOIN genre ON genre_musicains.genre_id = genre.id
    GROUP BY name_genre;
    """).fetchall()
pprint(select_1)


# 2 количество треков, вошедших в альбомы 2019-2020 годов
select_2 = connection.execute("""
    SELECT a.year_release_album,COUNT(name_track) FROM albums a
    JOIN track t  ON a.id = t.album_id
    WHERE a.year_release_album  >= 2019 AND a.year_release_album <= 2020
    GROUP BY a.year_release_album;
    """).fetchall()
pprint(select_2)


#3  средняя продолжительность треков по каждому альбому;
select_3 = connection.execute("""
    SELECT name_album,AVG(duration) FROM albums a
    JOIN track t  ON a.id = t.album_id
    GROUP BY name_album;
    """).fetchall()
pprint(select_3)


#4 все исполнители, которые не выпустили альбомы в 2020 году;
select_22 = connection.execute("""
    SELECT ma.musician_id,a.year_release_album FROM albums a
    JOIN musicians_albums ma  ON a.id = ma.album_id
    JOIN musicians m  ON ma.musician_id = m.id
    WHERE a.year_release_album != 2020;
    """).fetchall()
pprint(select_22)


#5 названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
select_5 = connection.execute("""
        SELECT name_digest FROM digets d
        JOIN composition_digets cd  ON d.id = cd.digest_id
        JOIN track t  ON cd.track_id = t.id
        JOIN albums a  ON t.album_id = a.id
        JOIN musicians_albums ma  ON a.id = ma.album_id
        JOIN musicians m  ON ma.musician_id = m.id
        WHERE name_musicians LIKE 'Тимати';
        """).fetchall()
pprint(select_5)


#6 название альбомов, в которых присутствуют исполнители более 1 жанра;
select_6 = connection.execute("""
        SELECT name_album FROM albums a
        JOIN musicians_albums ma  ON a.id = ma.album_id
        JOIN musicians m  ON ma.musician_id = m.id
        JOIN genre_musicains gm  ON m.id = gm.musician_id
        GROUP BY gm.musician_id, a.name_album
        HAVING count(gm.genre_id) > 1;
        """).fetchall()
pprint(select_6)


#7 наименование треков, которые не входят в сборники;
select_7 = connection.execute("""
        SELECT name_track FROM track t
        LEFT JOIN composition_digets cd ON t.id = cd.track_id
        WHERE cd.track_id IS NULL;
        """).fetchall()
pprint(select_7)
#

#8 исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
select_8 = connection.execute("""
        SELECT ma.musician_id, t.duration FROM musicians m
        JOIN musicians_albums ma ON m.id = ma.musician_id
        JOIN albums a ON ma.album_id = a.id
        JOIN track t ON a.id = t.album_id
        WHERE t.duration IN (SELECT MIN(duration) FROM track)
        """).fetchall()
pprint(select_8)


#9 название альбомов, содержащих наименьшее количество треков.
select_9 = connection.execute('''
    SELECT a.name_album, COUNT(t.id) FROM albums a
    JOIN track t  ON a.id = t.album_id
    GROUP BY a.name_album
    HAVING count(t.id) in (
        SELECT COUNT (t.id)
        FROM albums a
        JOIN track t  ON a.id = t.album_id
        GROUP BY a.name_album
        ORDER BY count(t.id)
        LIMIT 1)
    ''').fetchall()
pprint(select_9)

