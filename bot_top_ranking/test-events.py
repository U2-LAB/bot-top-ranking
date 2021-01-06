import os

from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2_pgevents.trigger import install_trigger, \
    install_trigger_function, uninstall_trigger, uninstall_trigger_function
from psycopg2_pgevents.event import poll, register_event_channel, \
    unregister_event_channel

load_dotenv()

connection = connect(
    database=os.getenv("NAME_DB"), 
    user=os.getenv("USER_DB"), 
    password=os.getenv("PASSWORD_DB"),
    host=os.getenv("HOST_DB"), 
    port=os.getenv("PORT_DB")
)
connection.autocommit = True

install_trigger_function(connection)
install_trigger(connection, 'music')
register_event_channel(connection)

try:
    print('Listening for events...')
    while True:
        for evt in poll(connection):
            print('New Event: {}'.format(evt))
except KeyboardInterrupt:
    print('User exit via Ctrl-C; Shutting down...')
    unregister_event_channel(connection)
    uninstall_trigger(connection, 'music')
    uninstall_trigger_function(connection)
    print('Shutdown complete.')