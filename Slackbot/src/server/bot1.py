# -*- coding: utf-8 -*-
from chatterbot import ChatBot

__all__ = "chatbot_1"

chatbot_1 = ChatBot(
    name="HAL 9000",
    input_adapter="input.SlackChat",
    output_adapter="output.SlackChat",
    database='database.db',
    )

# test bot 1
if __name__ == "__main__":
    # The following loop will execute each time the user enters input
    while True:
        try:
            # We pass None to this method because the parameter
            # is not used by the TerminalAdapter
            bot_input = chatbot_1.get_response(None)

        # Press ctrl-c or ctrl-d on the keyboard to exit
        except (KeyboardInterrupt, EOFError, SystemExit):
            break


