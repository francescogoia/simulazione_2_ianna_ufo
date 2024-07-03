from database.DB_connect import DBConnect



class DAO():
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select distinct(year (s.`datetime`)) as anno
            from sighting s
            order by anno desc
        """
        result = []
        cursor.execute(query)
        for row in cursor:
            result.append(row["anno"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllShapes():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select distinct shape
            from sighting s 
        """
        result = []
        cursor.execute(query)
        for row in cursor:
            result.append(row["shape"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(forma, anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select distinct s.city 
            from sighting s 
            where s.shape = %s and year(s.`datetime`) = %s
        """
        result = []
        cursor.execute(query, (forma, anno, ))
        for row in cursor:
            result.append(row["city"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(forma, anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select s1.city as c1, s2.city as c2, count(distinct s1.id) + count(distinct s2.id) as peso
            from sighting s1, sighting s2
            where s1.shape = %s and s1.shape = s2.shape and year(s1.`datetime`) = %s and year(s1.`datetime`) = year(s2.`datetime`)
                and month(s1.`datetime`) = month(s2.`datetime`)
	            and s1.id < s2.id and s1.city != s2.city
            group by s1.city, s2.city
        """
        result = []
        cursor.execute(query, (forma, anno, ))
        for row in cursor:
            result.append((row["c1"], row["c2"], row["peso"]))
        cursor.close()
        conn.close()
        return result






