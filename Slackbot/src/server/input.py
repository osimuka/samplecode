from __future__ import unicode_literals
from time import sleep
import json
from chatterbot.input import InputAdapter
from chatterbot.conversation import Statement

__all__ = "SlackChat"


def read_startup_file():
    with open("credentials.json") as data_file:
        data = json.load(data_file)
    return data

credentials = read_startup_file()


class SlackChat(InputAdapter):
    """
        An input adapter that allows a ChatterBot instance to get
        input statements from a Slack chat.
        """

    def __init__(self, **kwargs):
        super(SlackChat, self).__init__(**kwargs)

        self.host = kwargs.get('host', 'https://slack.com')
        # credentials
        self.token = kwargs.get('token', credentials['token'])
        self.channel = kwargs.get('channel', credentials['id'])
        self.name = kwargs.get('name', 'bot')
        # set initial conversation id to 0 if no conversation has started yet
        self.thread_id = kwargs.get('thread_id', '0')
        if self.get_most_recent_message():
            self.thread_id = kwargs.get(
                'thread_id', self.get_most_recent_message()['ts']
            )

    def get_most_recent_message(self):
        from slackclient import SlackClient
        response_handler = SlackClient(self.token)
        thread = response_handler.api_call(
            method="channels.history",
            token=self.token,
            channel=self.channel,
            ts=self.thread_id
        )
        self.logger.info('retrieving most recent messages from channel{}'.format(
            self.channel
        ))
        if thread.get('ok'):
            data = json.loads(json.dumps(thread))
            if data['messages']:
                # return most recent message
                return data['messages'][0]
        return None

    def process_input(self, statement):

        new_message = False
        data = None
        while not new_message:
            data = self.get_most_recent_message()
            # check if its not the bot replying to itself
            if data and 'user' in data.keys():
                new_message = True
            else:
                pass
            sleep(3.0)

        text = data['text']
        statement = Statement(text)
        self.logger.info('processing user statement {}'.format(statement))

        return statement

