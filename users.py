import argparse
from models import User
from psycopg2 import connect
from clcrypto import check_password


def create_user(cursor, username, password):
    if not User.load_user_by_username(cursor, username):
        if len(password) >= 8:
            new_user = User(username, password)
            new_user.save_to_db(cursor)
            print("User created!")
        else:
            print("Password is too short")
    else:
        print("User already exists!")


def update_user_password(cursor, username, password, newpass):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print("User does not exists!")
    else:
        if check_password(password, user.hashed_password):
            if len(password) < 8:
                print("New password is too short!")
            else:
                user.set_password(newpass)
                user.save_to_db(cursor)
                print("User password updated!")
        else:
            print("Password or username not correct!")


def delete_user(cursor, username, password):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print("User does not exists!")
    else:
        if check_password(password, user.hashed_password):
            user.delete(cursor)
            print("User deleted!")
        else:
            print("Password or username not correct!")


def list_users(cursor):
    users = User.load_all_users(cursor)
    print("List of users:")
    for single_user in users:
        print(single_user.username)


if __name__ == '__main__':
    try:
        cnx = connect(user="postgres", password="coderslab", host="localhost", database="workshop")
        cnx.autocommit = True
        cursor = cnx.cursor()
    except OperationalError:
        print("Connection to database error!")

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--newpass", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="list users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user password", action="store_true")

args = parser.parse_args()
if args.username and args.password and (not args.list and not args.delete and not args.edit and not args.newpass):
    create_user(cursor, args.username, args.password)
elif args.username and args.password and args.edit and args.newpass and (not args.list and not args.delete):
    update_user_password(cursor, args.username, args.password, args.newpass)
elif args.username and args.password and args.delete and (not args.edit and not args.newpass and not args.list):
    delete_user(cursor, args.username, args.password)
elif args.list and (not args.username and not args.password and not args.edit and not args.newpass and not args.delete):
    list_users(cursor)
else:
    parser.print_help()
