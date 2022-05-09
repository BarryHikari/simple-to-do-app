from argparse import ArgumentParser
import sqlite3

parser = ArgumentParser(description='Simple TODO App')
parser.add_argument('--install', help='Installation! WARNING, this may clear data base!')
parser.add_argument('--add', help='Add new task')
parser.add_argument('--list', help='Write tasks to do out', action='store_true')
parser.add_argument('--toggle', help='Change task status')

args = parser.parse_args()

connection = sqlite3.connect('to_do.db')
cursor = connection.cursor()

if args.install:
    print('Installing programme...')
    cursor.execute('DROP TABLE todos')
    cursor.execute('CREATE TABLE todos(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, is_done BOOLEAN)')
    connection.commit()

if args.add is not None:
    print('Adding...')
    title = args.add
    cursor.execute('INSERT INTO todos(title, is_done) VALUES(?, false)', (title, ))
    connection.commit()

if args.toggle is not None:
    print('Changing...')
    query = cursor.execute('SELECT is_done FROM todos WHERE id=?', (args.toggle,))
    is_done = query.fetchone()
    if is_done is None:
        print('Task do not exist!')
    elif is_done[0] == 1:
        print('Changing to undone!')
        new_is_done = 0
    elif is_done[0] == 0:
        print('Changing to done!')
        new_is_done = 1
    
    cursor.execute('UPDATE todos SET is_done=? WHERE id=?', (new_is_done, args.toggle))
    connection.commit()
        

if args.list:
    for todo_id, title, is_done in cursor.execute('SELECT id, title, is_done FROM todos'):
        print(f'{todo_id} \t {title} \t {"[V]" if is_done else "[]"}')


