# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from config import setting

__all__ = ["chatbot_2"]


chatbot_2 = ChatBot(
    name="Wall-E",
    input_adapter=setting["INPUT_ADAPTER"],
    output_adapter=setting["OUTPUT_ADAPTER"],
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
    )

chatbot_2.train('chatterbot.corpus.english')

# test bot 2
if __name__ == "__main__":

    print "{} is now connected".format(chatbot_2.name)
    # The following loop will execute each time the user enters input
    while True:
        try:
            # We pass None to this method because the parameter
            # is not used by the TerminalAdapter
            bot_input = chatbot_2.get_response(None)

        # Press ctrl-c or ctrl-d on the keyboard to exit
        except (KeyboardInterrupt, EOFError, SystemExit):
            break
