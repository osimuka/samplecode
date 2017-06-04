from chatterbot import ChatBot

__all__ = "chatbot_2"


chatbot_2 = ChatBot(
    name="Wall-E",
    input_adapter="chatterbot.input.TerminalAdapter",
    output_adapter="chatterbot.output.TerminalAdapter",
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
    )

chatbot_2.train('chatterbot.corpus.english.greetings')

# test bot 2
if __name__ == "__main__":

    print "You are now connected with {}".format(chatbot_2.name)
    # The following loop will execute each time the user enters input
    while True:
        try:
            # We pass None to this method because the parameter
            # is not used by the TerminalAdapter
            bot_input = chatbot_2.get_response(None)

        # Press ctrl-c or ctrl-d on the keyboard to exit
        except (KeyboardInterrupt, EOFError, SystemExit):
            break
