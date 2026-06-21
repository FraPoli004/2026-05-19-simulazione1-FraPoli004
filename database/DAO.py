from database.DB_connect import DBConnect
from model.genre import Genre
from model.artista import Artista


class DAO():

    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM genre"
        cursor.execute(query)

        for row in cursor:
            result.append(Genre(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(g : int):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.*
        from  track t, album al, artist a
        WHERE a.ArtistId = al.ArtistId
        AND al.AlbumId = t.AlbumId
        AND t.GenreId = %s
        order by a.Name """
        cursor.execute(query,(g,))

        for row in cursor:
            result.append(Artista(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT al1.ArtistId AS a1, al2.ArtistId AS a2
                    FROM invoice i1, invoiceline il1, track t1, album al1,
                    invoice i2, invoiceline il2, track t2, album al2
                    WHERE i1.InvoiceId = il1.InvoiceId
                      AND il1.TrackId  = t1.TrackId
                      AND t1.AlbumId   = al1.AlbumId
                      AND i2.InvoiceId = il2.InvoiceId
                      AND il2.TrackId  = t2.TrackId
                      AND t2.AlbumId   = al2.AlbumId
                      AND i1.CustomerId = i2.CustomerId         
                      AND al1.ArtistId  < al2.ArtistId        
                      AND al1.ArtistId IN (SELECT DISTINCT alx.ArtistId
                       FROM album alx, track tx
                       WHERE alx.AlbumId = tx.AlbumId AND tx.GenreId = %s)
                       AND al2.ArtistId IN (SELECT DISTINCT aly.ArtistId
                       FROM album aly, track ty
                       WHERE aly.AlbumId = ty.AlbumId AND ty.GenreId = %s)"""
        cursor.execute(query)

        for row in cursor:
            result.append((row["a1"], row["a2"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllPopolarita():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT al.ArtistId AS artista, SUM(il.Quantity) AS popolarita
                    FROM invoiceline il, track t, album al
                    WHERE il.TrackId = t.TrackId
                    AND t.AlbumId = al.AlbumId
                    GROUP BY al.ArtistId"""
        cursor.execute(query)

        for row in cursor:
            result.append((row["artista"], row["popolarita"]))

        cursor.close()
        conn.close()
        return result

