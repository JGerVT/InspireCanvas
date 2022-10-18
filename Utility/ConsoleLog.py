from datetime import datetime
from Settings.settings import *



def log(name: str, description = ""):
    """Logs actions taken by the user, with a timestamp

    Args:
        name (str): name of log
        description (str, optional): description of log. Defaults to "".
    """
    log = getDateTime() + ": " + name + " - " + description
    # print(log)

    # Write to log file
    logFile = open(softwareLogLocation, 'a')
    logFile.write(log)
    logFile.write("\n")
    logFile.close()

def error(errorName: str, description = ""):
    log("[ERROR] " + errorName, description)    

def alert(errorName: str, description = ""):
    log("[ALERT] " + errorName, description)    

def warning(debugName: str, description = ""):
    log("[WARNING] " + debugName, description)    

def debug(debugName: str, description = ""):
    log("[DEBUG] " + debugName, description)    


def getDateTime():
    return datetime.now().__str__()