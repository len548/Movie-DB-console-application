from classes import database, console


def main():
    try:
        print("Enter mySQL database details to connect.")
        host = input("host name: ")
        user = input("user name: ")
        password = input("password: ")
        print("Connecting database..")
        db = database.Database(host, user, password)
        db.connect()
        print("Successful Connection with database.")
        cons = console.Console(db)
        cons.print_menu()
        while True:
            try:
                cmd = input("Enter a command: ")
                if cmd == "close":
                    db.close()
                    exit(0)
                else:
                    cons.read_cmd(cmd)
            except ValueError as ve:
                print(ve)
                print('Try again!')

    except database.DataBaseConnectionError as dbce:
        print("Failed to connect with database.")
        exit(-1)


if __name__ == "__main__":
    main()