from chatterbot import ChatBot


class Bot1(object):
    name = "HAL 9000"
    chatbot = ChatBot(
        name,
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
        input_adapter='client.input_slackchat.InputAdapter',
        output_adapter='client.output_slackchat.OutputAdapter',
    )
    chatbot.train('chatterbot.corpus.english')


