"""
Description: This python file provides console logging functionality.  

Date Created: 10/18/22 
Date Updated: 11/22/22
"""

from datetime import datetime
from Settings.settings import *

softwareLogLocation = "Data\softwareLog.log"

def log(name: str, description = ""):
    """Logs actions taken by the user, with a timestamp

    Args:
        name (str): name of log
        description (str, optional): description of log. Defaults to "".
    """
    log = getDateTime() + ": " + name + " - " + description

    # Write to log file
    try:
        with open(softwareLogLocation, 'a') as logFile:
            logFile.write(log)
            logFile.write("\n")
            logFile.close()
    except:
        print("Error File not found.")

    return log

def error(errorName: str, description = ""):
    log_ = log("[ERROR] " + errorName, description)    
    print(log_) # Print errors to canvas

def alert(errorName: str, description = ""):
    log("[ALERT] " + errorName, description)    

def warning(debugName: str, description = ""):
    log("[WARNING] " + debugName, description)    

def debug(debugName: str, description = ""):
    log("[DEBUG] " + debugName, description)    


def getDateTime():
    return datetime.now().__str__()