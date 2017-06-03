from bots.bot1 import Bot1

bot_1 = Bot1()


def connect():
    print "You are now connected with the bot\n"


def disconnect():
    print "You are now disconnected"


def main():
    connect()
    while True:
        input = raw_input(">")
        response = bot_1.chatbot.process_input_statement(input)
        if input == "@disconnect":
            break
        print response
    disconnect()

if __name__ == "__main__":
    main()
