from __future__ import unicode_literals
import socket
import sys
#from time import sleep
from chatterbot.input import InputAdapter
from chatterbot.output import OutputAdapter
from chatterbot.conversation import Statement

server_address = ('localhost', 10000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Listen for incoming connections
sock.bind(server_address)
sock.listen(1)
connection, client_address = sock.accept()


class SlackInputAdapter(InputAdapter):
    """
        An input adapter that allows a ChatterBot instance to get
        input statements from a HipChat room.
        """

    def __init__(self, **kwargs):
        super(SlackInputAdapter, self).__init__(**kwargs)

    def process_input(self, *args, **kwargs):
        user_input = ""
        print >> sys.stderr, 'connection from', client_address
        # Receive the data in small chunks
        while True:
            data = connection.recv(1024)
            print >> sys.stderr, 'received "%s"' % data
            if data:
                user_input += data
            else:
                print >> sys.stderr, 'no more data from', client_address
                break
            return Statement(user_input)


class SlackOutputAdapter(OutputAdapter):

    def __init__(self, **kwargs):
        super(SlackOutputAdapter, self).__init__(**kwargs)

    def process_response(self, statement, session_id=None):
        connection.sendall(statement.text)
        return statement
