class Movie:
    def __init__(self, movie_id, title, director_name, release_year, length_minutes):
        self.movie_id = movie_id
        self.title = title
        self.director_name = director_name
        self.release_year = release_year
        self.length_minutes = length_minutes
        self.actors = []

