# MovieDB - Nokia DevOps Internship Assignment

## Description
A console application that can list and alter a database of movies, directors and actors.

- With "d -p" users can delete people from the database. After -p switch, a string should be added. If it is the exact name of a person in the database, deletes them, and also deletes them from every movie they starred in. If they are a director in a movie, then we cannot delete them and the program should notify the user about this. The program should also notify the user if the person cannot be found in the database.

## Used envrionment:
- IDE: IntelliJ
- Database: MySQL
## Requirement Before Run the Project
### On MySQL: 
* Run the attached sql script (nokia2023hw_sample_database_setup.sql) on MySQL.
  * It creates database schema and necessary tables, and insert some sample data into the tables.

## Note from Me:
You can run test cases on test_console.py and test_database.py. But because I did not have enough time, implemented test cases are not enough to prove only little of functionalities and error handling in those classes. I just leave them to implement the rest later, so do not consider that much into my application please.. 