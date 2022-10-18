"""
Description:    This python file is a Utility file that get's data from the JSON database.


Date Created: 9/21/22 
Date Updated: 10/17/22
"""

# Imports
import json
from os import path
from time import time

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from Utility.UtilityFunctions import GenerateID

def LoadJSON(fileLocation):
    """Load the JSON data

    Args:
        fileLocation (str) : Name of the location of the JSON data
    
    Return:
        Returns the data as a Python Object. 
    """
    with open(fileLocation) as f:
        ProjectJSONObject =  json.load(f)["Project"]
        return ProjectJSONObject

def GetProjectName(JSONObject):
    """Get and return the project name"""
    return JSONObject["projectName"]

def GetSelectedTab(JSONObj):
    """Get and return the selected tab from the JSON object"""
    return JSONObj["selectedTab"]

def LoadTabs(JSONObj):
    """Creates a dictionary of all tabs in the JSON Object"""
    tabDict = dict()
    for data in JSONObj["tabs"]:
        tabDict[data["tabID"]] = data
    return tabDict

def GetTabs(JSONObject):
    """Return tabs from JSON Object"""
    return JSONObject["tabs"]

def LoadNodes(JSONObj):
    """Creates and returns a dictionary for the nodes in the .json file
    Args:
        JSONObj: The entire JSON object. 
    Return: 
        Returns the nodeDict (dictionary of all nodes) 
    """
    nodeDict = dict()

    for node in JSONObj["nodes"]:   # For each node in ["nodes"], set the nodeID as the key
        nodeDict[node["nodeID"]] = node
    return nodeDict


def CreateImageNode(imagePath, nodeName = "Image_Node"):
    if path.exists(imagePath):
        node = {
            "nodeType": nodeName,
            "nodeName": "Image",
            "nodeID": GenerateID(),
            "creationTime": time(),
            "imagePath": imagePath
        }
        return node

    else:
        print("CreateImageNode: Invalid Path")
        raise Exception("CreateImageNode: Invalid Path")

def CreateCanvasItem(nodeID: str, itemPos: QPointF, itemScale:float):
    canvasItem = {
        "nodeID": nodeID,
        "itemPos": [itemPos.x(), itemPos.y()],
        "itemScale": itemScale
    }
    return canvasItem