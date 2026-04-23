import json

def check_config():
    try:
        with open("config.json", "r") as file:
            json.load(file)
            print("System Ready")
    except FileNotFoundError:
        default_settings = {"theme": "Black", "language": "Arabic"}
        with open("config.json", "w") as file:
            json.dump(default_settings, file)

check_config()