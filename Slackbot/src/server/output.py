from __future__ import unicode_literals
from input import credentials
from chatterbot.output import OutputAdapter

__all__ = "SlackChat"


class SlackChat(OutputAdapter):
    """
        An input adapter that allows a ChatterBot instance to get
        input statements from a Slack chat.
        """

    def __init__(self, **kwargs):
        super(SlackChat, self).__init__(**kwargs)
        self.host = kwargs.get('host', 'https://slack.com')
        self.channel = kwargs.get('channel', credentials['id'])
        self.token = kwargs.get('token', credentials['token'])
        self.thread_id = kwargs.get('thread_id')
        self.username = kwargs.get('name')

    def send_message(self, message):
        """
        Send a message to SlackChat.
        https://api.slack.com/methods/chat.postMessage
        """
        from slackclient import SlackClient
        response_handler = SlackClient(self.token)

        response_handler.api_call(
            method="chat.postMessage",
            token=self.token,
            channel=self.channel,
            text=message,
            ts=self.thread_id,
            username=self.username
        )

    def process_response(self, statement, session_id=None):
        self.send_message(statement.text)
        return statement

