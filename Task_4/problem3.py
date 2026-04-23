def write_log(message):
    with open("log.txt", "a") as file:
        file.write(message + "\n")


def read_logs():
    with open("log.txt", "r") as file:
        for line in file:
            print(line.strip())


write_log("System started")
write_log("User logged in")

read_logs()