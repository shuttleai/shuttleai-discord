from dateutil import tz
from datetime import datetime
from pystyle import *


class Color:
    gray = "\033[90m"
    reset = "\033[0m" 
    green = "\033[38;5;120m"
    red = "\033[1m\x1b[38;5;203m"
    orange = Colors.orange
    light_purple = "\033[38;5;99m"
    pink = Colors.pink
    blue = "\033[38;5;75m"
    light_pink = "\033[38;5;213m"


class log:

    @staticmethod
    def log(text: str, **kwargs):
        log_message = f"{Color.reset}{text} " + " ".join([f"{Color.gray}{key}={Color.reset}{value}" for key, value in kwargs.items()])
        print(Color.gray + datetime.now(tz.tzlocal()).strftime('%I:%M:%S'), log_message)
    
    @staticmethod
    def success(text: str, **kwargs):
        message = f"{Color.gray}{datetime.now(tz.tzlocal()).strftime('%I:%M:%S')}{Color.reset} {Color.green}INF{Color.reset}{Color.gray} > {Color.reset}{text} " + " ".join([f"{Color.gray}{key}={Color.reset}{value}" for key, value in kwargs.items()])
        message = message.replace(" [", f" {Color.gray}[{Color.blue}")
        message = message.replace("]", f"{Color.gray}]{Color.reset}")
        print(message)

    @staticmethod
    def system(text: str, **kwargs):
        print(f"{Color.gray}{datetime.now(tz.tzlocal()).strftime('%I:%M:%S')}{Color.reset} {Color.light_purple}SYS{Color.reset}{Color.gray} > {Color.reset}{text} " + " ".join([f"{Color.gray}{key}={Color.reset}{value}" for key, value in kwargs.items()]))

    @staticmethod
    def wavelink(text: str, **kwargs):
        print(f"{Color.gray}{datetime.now(tz.tzlocal()).strftime('%I:%M:%S')}{Color.reset} {Color.blue}WAV{Color.reset}{Color.gray} > {Color.reset}{text} " + " ".join([f"{Color.gray}{key}={Color.reset}{value}" for key, value in kwargs.items()]))

    @staticmethod
    def cog(text: str, **kwargs):
        print(f"{Color.gray}{datetime.now(tz.tzlocal()).strftime('%I:%M:%S')}{Color.reset} {Color.pink}COG{Color.reset}{Color.gray} > {Color.reset}{text} " + " ".join([f"{Color.gray}{key}={Color.reset}{value}" for key, value in kwargs.items()]))

    @staticmethod
    def error(text: str, **kwargs):
        print(f"{Color.gray}{datetime.now(tz.tzlocal()).strftime('%I:%M:%S')}{Color.reset} {Color.red}ERR{Color.reset}{Color.gray} > {Color.reset}{text} " + " ".join([f"{Color.gray}{key}={Color.reset}{value}" for key, value in kwargs.items()]))

    @staticmethod
    def warn(text: str, **kwargs):
        print(f"{Color.gray}{datetime.now(tz.tzlocal()).strftime('%I:%M:%S')}{Color.reset} {Colors.orange}WRN{Color.reset}{Color.gray} > {Color.reset}{text} " + " ".join([f"{Color.gray}{key}={Color.reset}{value}" for key, value in kwargs.items()]))

    @staticmethod
    def message(text: str, **kwargs):
        message = f"{Color.gray}{datetime.now(tz.tzlocal()).strftime('%I:%M:%S')}{Color.reset} {Color.light_pink}MSG{Color.reset}{Color.gray} > {Color.reset}{text} " + " ".join([f"{Color.gray}{key}={Color.reset}{value}" for key, value in kwargs.items()])
        message = message.replace(" [", f" {Color.gray}[{Color.blue}")
        message = message.replace("]", f"{Color.gray}]{Color.reset}")
        print(message)

    @staticmethod
    def img(text: str, **kwargs):
        colored_text = text.replace('"', f'{Color.light_purple}"{Color.reset}').replace('"', f'{Color.light_purple}"{Color.reset}')
        print(f"{Color.gray}{datetime.now(tz.tzlocal()).strftime('%I:%M:%S')}{Color.reset} {Color.light_purple}IMG{Color.reset}{Color.gray} > {Color.reset}{colored_text} " + " ".join([f"{Color.gray}{key}={Color.reset}{value}" for key, value in kwargs.items()]))
