import os.path
import json

credentials_path = os.path.abspath("src/..")

if os.path.split(credentials_path)[1] != "src":
    credentials_path = os.path.split(credentials_path)[0]

credentials_path += "\credentials.json"


def read_startup_file():
    with open(credentials_path) as data_file:
        data = json.load(data_file)
        if data:
            return data
    raise ValueError("No slack credentials inside 'credentials.json'")

credentials = read_startup_file()

setting = {

    "INPUT_ADAPTER": "input.SlackChat",
    "OUTPUT_ADAPTER": "output.SlackChat",
    "TOKEN": credentials["token"],
    "CHANNEL": credentials["id"],
    "DM_CHANNEL": credentials["dm"],
    "CLIENT_ID": credentials["client_ID"],
    "USER": credentials["user"]
}
