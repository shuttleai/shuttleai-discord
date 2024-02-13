import datetime
import pytz

# ANSI escape codes for coloring text output in the terminal
class TerminalColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GRAY = '\033[90m'
    DARKGRAY = '\033[30m'
    LIGHTGRAY = '\033[37m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    DARKPURPLE = '\033[34m'
  
class log:
    def _log(self, level, message, color):
        pst_timezone = pytz.timezone('America/Los_Angeles') # Change this to your timezone, mine is PST so I use America/Los_Angeles
        timestamp = datetime.datetime.now(pst_timezone).strftime('%I:%M:%S')
        formatted_message = f"{TerminalColor.GRAY}{TerminalColor.BOLD}{timestamp} {color}{TerminalColor.BOLD}{level}{TerminalColor.ENDC}  {message}"
        formatted_message = formatted_message.replace(" [", f" {TerminalColor.GRAY}{TerminalColor.BOLD}[{TerminalColor.DARKPURPLE}")
        formatted_message = formatted_message.replace("]", f"{TerminalColor.GRAY}{TerminalColor.BOLD}]{TerminalColor.ENDC}")
        print(formatted_message)

    def info(self, message):
        self._log("INF", message, TerminalColor.OKBLUE)

    def error(self, message):
        self._log("ERR", message, TerminalColor.FAIL)

    def success(self, message):
        self._log("YES", message, TerminalColor.OKGREEN)

    def fail(self, message):
        self._log("NO", message, TerminalColor.FAIL)

    def warn(self, message):
        self._log("WARN", message, TerminalColor.WARNING)

    def debug(self, message):
        self._log("DBG", message, TerminalColor.OKCYAN)

log = log()