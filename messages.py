import argparse
from models import User, Message
from psycopg2 import connect
from clcrypto import check_password


def list_messages(cursor, username, password):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print("User does not exists!")
    else:
        if check_password(password, user.hashed_password):

            messages = Message.load_all_messages(cursor, user.id)
            if messages:
                print("Messages for you:")
            else:
                print("There is no messages for you!")
            for message in messages:
                user_from = User.load_user_by_id(cursor, message.from_id)
                print(f"Author: {user_from.username}, sent: {message.creation_date} Content:\n{message.text}")
        else:
            print("Password or username not correct!")
            
def send_message(cursor, username, password, user_to_name, text):
    user = User.load_user_by_username(cursor, username)
    user_to = User.load_user_by_username(cursor, user_to_name)
    if not user or not user_to:
        print("At leaat one of users does not exists!")
    else:
        if check_password(password, user.hashed_password):
            if len(text) > 255:
                print("Message too long!")
            else:
                messsage = Message(user.id, user_to.id, text)
                messsage.save_to_db(cursor)
                print("Message sent!")
        else:
            print("Password or username not correct!")


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
parser.add_argument("-t", "--to", help="username of message receiver")
parser.add_argument("-s", "--send", help="content of message to send")
parser.add_argument("-l", "--list", help="list users", action="store_true")

args = parser.parse_args()
if args.username and args.password and args.list and (not args.to and not args.send):
    list_messages(cursor, args.username, args.password)
elif args.username and args.password and (not args.list) and args.to and args.send:
    send_message(cursor, args.username, args.password, args.to, args.send)
else:
    parser.print_help()
