import platform
from datetime import datetime

def log_system_info():
    os_type = platform.system()
    current_time = datetime.now()

    with open("sys_log.txt", "a") as file:
        file.write(f"OS: {os_type}, Time: {current_time} \n")

def main():
    log_system_info()

if __name__ == "__main__":
    main()