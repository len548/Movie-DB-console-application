"""Database class
    handles communication with MySQL database
"""

import mysql.connector as mysql
from src.classes.movie import Movie
from src.classes.people import People


class Database:
    def __init__(self, host, user, passwd):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd
            )
        except mysql.errors.DatabaseError as dbe:
            raise DataBaseConnectionError()

    def close(self):
        self.connection.close()

    def get_movie_data(self):
        cursor = self.connection.cursor()
        cursor.execute("USE nokia2023hw;")
        query = "SELECT * FROM movies order by title"
        cursor.execute(query)

        movies_data = cursor.fetchall()
        movies = []
        for row in movies_data:
            movie = Movie(*row)
            movies.append(movie)

        query = "SELECT m.movie_id, p.name, p.birth_year FROM movie_actors ma JOIN people p ON ma.actor_id = p.person_id JOIN movies m ON ma.movie_id = m.movie_id"
        cursor.execute(query)

        # Fetch all rows from the result set
        actors_data = cursor.fetchall()

        # Associate actors with movies
        for actor_data in actors_data:
            for movie in movies:
                if movie.movie_id == actor_data[0]:
                    name = actor_data[1]
                    birth_year = actor_data[2]
                    actor = People(name, birth_year)
                    movie.actors.append(actor)

        cursor.close()
        return movies

    def add_people(self, name, year_of_birth):
        cursor = self.connection.cursor()
        cursor.execute("USE nokia2023hw;")
        try:
            query = "INSERT INTO people (name, birth_year) VALUES (%s, %s)"
            val = (name, year_of_birth)
            cursor.execute(query, val)
            self.connection.commit()
        except mysql.errors.DatabaseError as dbe:
            raise DataBaseError(f"Error executing database query: {dbe}")

        finally:
            cursor.close()

    def person_exists(self, person_name):
        try:
            cursor = self.connection.cursor()
            cursor.execute("USE nokia2023hw;")
            cursor.execute("SELECT person_id FROM people WHERE name = %s", (person_name,))
            exists = cursor.fetchone() is not None
            cursor.close()
            return exists
        except mysql.errors.DatabaseError as dbe:
            raise DataBaseError(f"Error executing database query: {dbe}")

    def add_movie(self, title, director, release_year, length_minutes, actors):
        cursor = self.connection.cursor()
        cursor.execute("USE nokia2023hw;")
        try:
            # Insert movie data into movies table
            cursor.execute("INSERT INTO movies (title, director_name, release_year, length_minutes) VALUES (%s, %s, %s, %s)",
                           (title, director, release_year, length_minutes))

            # Get the movie_id of the newly added movie
            cursor.execute("SELECT LAST_INSERT_ID()")
            movie_id = cursor.fetchone()[0]

            # Insert actors into movie_actors table
            for actor_name in actors:
                if not self.person_exists(actor_name):
                    raise ValueError(f"Actor '{actor_name}' does not exist in the database.")

                cursor.execute("SELECT person_id FROM people WHERE name = %s", (actor_name,))
                actor_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO movie_actors (movie_id, actor_id) VALUES (%s, %s)", (movie_id, actor_id))

            # Commit the changes
            self.connection.commit()

        except mysql.errors.DatabaseError as dbe:
            raise DataBaseError(f"Error executing database query: {dbe}")

        finally:
            cursor.close()

    def delete_person(self, person_name):
        try:
            cursor = self.connection.cursor()
            cursor.execute("USE nokia2023hw;")
            # Check if the person exists in the people table
            cursor.execute("SELECT person_id FROM people WHERE name = %s", (person_name,))
            person_id = cursor.fetchone()

            if person_id is None:
                print(f"Person '{person_name}' not found in the database.")
                return False
            person_id = person_id[0]

            # Check if the person is a director in any movie
            cursor.execute("SELECT movie_id FROM movies WHERE director_name = %s", (person_name,))
            director_in_movie = cursor.fetchone()

            if director_in_movie is not None:
                print(f"Cannot delete '{person_name}' as they are a director in a movie.")
                return False

            # Use nextset() to consume any remaining result sets
            cursor.nextset()

            # Delete the person from movie_actors table
            cursor.execute("DELETE FROM movie_actors WHERE actor_id = %s", (person_id,))

            # Delete the person from people table
            cursor.execute("DELETE FROM people WHERE person_id = %s", (person_id,))

            self.connection.commit()
            cursor.close()
            return True
        except mysql.errors.DatabaseError as dbe:
            raise DataBaseError(f"Error executing database query: {dbe}")


class DataBaseError(Exception):
    pass


class DataBaseConnectionError(Exception):
    pass
