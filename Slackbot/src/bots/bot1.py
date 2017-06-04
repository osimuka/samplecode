from chatterbot import ChatBot

__all__ = "bot_1"


class Bot1(ChatBot):
    def __init__(self, **kwargs):
        super(Bot1, self).__init__(**kwargs)


bot_1 = Bot1(
    name="HAL 9000",
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
    )
bot_1.train('chatterbot.corpus.english')


