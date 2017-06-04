


def main():
    while True:
        input = raw_input(">>")
        response = "next"
        if input == "@disconnect":
            break
        print response

if __name__ == "__main__":
    main()
