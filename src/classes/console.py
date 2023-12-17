""" Console class
    validates input commands given by a user on a console
    and execute action corresponding to a valid command."""
import re

from src.classes.database import DataBaseError as DataBaseError


class Console:
    def __init__(self, db):
        self.db = db

    def print_menu(self):
        menu = "----------Menu------------------------------------------------------------------------------------------\n"
        l = 'Write "l" to list movies line by line following this format:\n ' + \
            "<title> by <director> in <year>, <length>\n\n"
        lv = 'Write "l -v" the entry for a movie will be shown in this format:\n' + \
             "<title> by <director> in <year>, <length> and starring actors\n\n"
        t_switch = "Add -t and after that between quotes a regex can be given to match the title with.\n"
        d_switch = "Add -d and after that between quotes a regex can be given to filter by the movie's director\n";
        a_switch = "Add -a and after that between quotes a regex can be given to filter by the movie's actor\n";
        la_switch = "Add -la lists the movies with ascending order by their length\n"
        ld_switch = "Add -ld lists the movies with descending order by their length\n"
        am_switch = '"a -m" allows to add new movie\n'
        ap_switch = '"a -p\" allows to add new people\n'
        dp_switch = '"d -p" users can delete people from the database\n'
        close = '"close" to close the program\n'

        print(
            menu + l + lv + t_switch + d_switch + a_switch + la_switch + ld_switch + \
            am_switch + ap_switch + dp_switch + close)

    # read_cmd(cmd) executes action based on a given command by a user.
    # It checks if the given command (cmd) is valid or not
    def read_cmd(self, cmd):
        cmd_tokens = self.split_command(cmd)
        arg_length = len(cmd_tokens)
        if cmd_tokens[0] == "l":
            i = 1
            switches = {'include_actors': False}
            while i < arg_length:
                try:
                    match cmd_tokens[i]:
                        case "-v":
                            switches['include_actors'] = True
                            i += 1
                        case "-t":
                            regex_token = cmd_tokens[i + 1]
                            if not regex_token.startswith('"') or not regex_token.endswith('"'):
                                raise ValueError(f"Regular expression not quoted correctly: {regex_token}")
                            regex_token = regex_token[1:-1]
                            if not self.is_valid_regex(regex_token):
                                raise ValueError(f"Invalid regular expression: {cmd_tokens[i + 1]}")
                            switches['-t'] = regex_token
                            i += 2
                        case "-d":
                            regex_token = cmd_tokens[i + 1]
                            if not regex_token.startswith('"') or not regex_token.endswith('"'):
                                raise ValueError(f"Regular expression not quoted correctly: {regex_token}")
                            regex_token = regex_token[1:-1]
                            if not self.is_valid_regex(regex_token):
                                raise ValueError(f"Invalid regular expression: {regex_token}")
                            switches['-d'] = regex_token
                            i += 2
                        case "-a":
                            regex_token = cmd_tokens[i + 1]
                            if not regex_token.startswith('"') or not regex_token.endswith('"'):
                                raise ValueError(f"Regular expression not quoted correctly: {regex_token}")
                            regex_token = regex_token[1:-1]
                            if not self.is_valid_regex(regex_token[i + 1]):
                                raise ValueError(f"Invalid regular expression: {regex_token[i + 1]}")
                            switches['-a'] = regex_token
                            i += 2
                        case "-la":
                            if '-ld' in switches:
                                raise ValueError("-la and -ld switch cannot be used together")
                            switches['-la'] = True
                            i += 1
                        case "-ld":
                            if '-la' in switches:
                                raise ValueError("-la and -ld switch cannot be used together")
                            switches['-ld'] = True
                            i += 1
                        case _:
                            '''this handles wrong format of the given command
                            (no parameter after -d or regexes are not quoted)'''
                            raise ValueError(f"Error - not supported switch '{cmd_tokens[i]}'")
                except IndexError:
                    raise ValueError(f"Error - searching keyword missing after {cmd_tokens[i]}")
            self.list_movies(switches)
        elif cmd_tokens[0] == "a":
            if arg_length == 1:
                raise ValueError("Error - '-p' or '-m' is missing")
            elif arg_length > 2:
                raise ValueError("Error - Unnecessary argument detected.")

            match cmd_tokens[1]:
                case '-p':
                    self.add_people()
                case '-m':
                    self.add_movie()
                case _:
                    raise ValueError(f"Error - Not supported switch '{cmd_tokens[1]}'")
        elif cmd_tokens[0] == "d":
            if arg_length == 2 and cmd_tokens[1] == '-p':
                try:
                    self.delete_people()
                except ValueError as ve:
                    raise ValueError(ve)
            else:
                raise ValueError(f"Error - command error after 'd'")
        else:
            raise ValueError(f"Error - Not supported operation : {cmd_tokens[0]}")

    def list_movies(self, switches):
        movies = self.db.get_movie_data()
        # apply conditions by given switches to a list of movies
        for switch in list(switches):
            match switch:
                case '-t':
                    keyword_regex = switches[switch]
                    movies = self.filter_by_title(movies, keyword_regex)
                case '-d':
                    keyword_regex = switches[switch]
                    movies = self.filter_by_director(movies, keyword_regex)
                case '-a':
                    keyword_regex = switches[switch]
                    movies = self.filter_by_actor(movies, keyword_regex)
                case '-la':
                    movies = self.sort_asc_by_length(movies)
                case '-ld':
                    movies = self.sort_dsc_by_length(movies)
                case _:
                    pass
        if switches['include_actors']:
            for movie in movies:
                print(f"{movie.title} by {movie.director_name} in {movie.release_year}, {movie.length_minutes}")
                print("      Starring:")
                for actor in movie.actors:
                    print(f"            - {actor.name} at age {movie.release_year - actor.birth_year}")
                print("---")
        else:
            for movie in movies:
                print(f"Movie ID: {movie.movie_id}")
                print(f"Title: {movie.title}")
                print(f"Director: {movie.director_name}")
                print(f"Release Year: {movie.release_year}")
                print(f"Length (minutes): {movie.length_minutes}")
                print("---")

    def filter_by_title(self, movies, keyword):
        regex = re.compile(keyword)
        filtered_movies = [movie for movie in movies if regex.match(movie.title)]
        return filtered_movies

    def filter_by_director(self, movies, keyword):
        regex = re.compile(keyword)
        filtered_movies = [movie for movie in movies if regex.match(movie.director_name)]
        return filtered_movies

    def filter_by_actor(self, movies, keyword):
        regex = re.compile(keyword)
        # filtered_movies = [movie for movie in movies if any(regex.match(actor.name) for actor in movie.actors)]
        filtered_movies = []
        for movie in movies:
            exist = False
            for actor in movie.actors:
                if regex.match(actor.name):
                    exist = True
                    break
            if exist:
                filtered_movies.append(movie)
        return filtered_movies

    def sort_asc_by_length(self, movies):
        sorted_movies = sorted(movies, key=lambda m: m.length_minutes)
        return sorted_movies

    def sort_dsc_by_length(self, movies):
        sorted_movies = sorted(movies, reverse=True, key=lambda m: m.length_minutes)
        return sorted_movies

    def add_people(self):
        try:
            name = input("Name: ")
            year_birth_str = input("Year of birth: ")
            year_birth = int(year_birth_str)
            if year_birth < 1900 or year_birth > 2023:
                raise ValueError("Year of birth has to be between 1900 and 2023")
            self.db.add_people(name, year_birth)
            print("Added the person successfully.")
        except ValueError:
            raise ValueError(f"Invalid integer input")

    def add_movie(self):
        # Get title
        title = input("> Title: ")

        # Get and validate length in hh:mm format
        while True:
            length_input = input("> Length: ")
            try:
                hours, minutes = map(int, length_input.split(':'))
                if 0 <= hours <= 99 and 0 <= minutes <= 59:
                    length = hours * 60 + minutes
                    break
                else:
                    print("> - Bad input format (hh:mm), try again!")
            except ValueError:
                print("> - Bad input format (hh:mm), try again!")

        # Get and validate director
        while True:
            director = input("> Director: ")
            if self.db.person_exists(director):
                break
            else:
                print(f"> - We could not find '{director}', try again!")

        # Get and validate release year
        while True:
            release_year_input = input("> Released in: ")
            try:
                release_year = int(release_year_input)
                if 1900 <= release_year <= 9999:
                    break
                else:
                    print("> - Invalid year, try again!")
            except ValueError:
                print("> - Invalid year, try again!")

        # Get and validate actors
        actors = []
        print("> Starring (type 'exit' to finish):")
        while True:
            actor = input("> ")
            if actor.lower() == 'exit':
                break
            elif self.db.person_exists(actor):
                actors.append(actor)
            else:
                print(f"> - We could not find '{actor}', try again!")

        # Add the new movie to the database
        self.db.add_movie(title, director, release_year, length, actors)
        print("The movie added successfully.")

    def delete_people(self):
        try:
            name = input("Name: ")
            if self.db.delete_person(name):
                print("The person deleted successfully.")
        except DataBaseError as dbe:
            raise ValueError(dbe)

    # helper functions in read_cmd(cmd)
    def split_command(self, input_string):
        tokens = re.findall(r'"(?:\\"|[^"])*"|\S+', input_string)
        return tokens

    def is_valid_regex(self, keyword):
        try:
            re.compile(keyword)
            return True
        except re.error:
            return False
