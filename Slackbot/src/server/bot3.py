from chatterbot import ChatBot

__all__ = "chatbot_3"

chatbot_3 = ChatBot(
    name="Agent Smith",
    input_adapter="server.SlackInputAdapter",
    output_adapter="server.SlackOutputAdapter",
    storage_adapter='chatterbot.storage.JsonFileStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
        ],
    trainer="chatterbot.trainers.ListTrainer",
    )

chatbot_3.train([
    'How can I help you?',
    'I want to create a chat bot',
    'You are about to enter the matrix?',
    'No, I have not'
])

# test bot 3
if __name__ == "__main__":

    print "You are now connected with {}".format(chatbot_3.name)
    # The following loop will execute each time the user enters input
    while True:
        try:
            # We pass None to this method because the parameter
            # is not used by the TerminalAdapter
            bot_input = chatbot_3.get_response(None)

        # Press ctrl-c or ctrl-d on the keyboard to exit
        except (KeyboardInterrupt, EOFError, SystemExit):
            break
