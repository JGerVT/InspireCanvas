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
from Settings.settings import * 

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


def CreateCIData(nodeID: str, itemPos: QPointF, itemScale:float):
    """Creates data for a new CI (CanvasItem)

    Args:
        nodeID (str): ID of the new CanvasItem
        itemPos (QPointF): position for the new Canvas Item to be set
        itemScale (float): scale for the new canvasItem

    Returns:
        Dict: returns a dictionary of nodeID, itemPos, and itemScale 
    """
    canvasItem = {
        "nodeID": nodeID,
        "itemPos": [itemPos.x(), itemPos.y()],
        "itemScale": itemScale
    }
    return canvasItem

def CreateTabData(tabName: str, tabID:str, canvasItems, viewportPos = [2500,2500], viewportZoom = 1, tabColor = defaultAccentColor):
    """Creates data for a new Tab

    Args:
        tabName (str): name of the new tab
        tabID (str): ID of the new tab
        canvasItems (_type_): List of CanvasItems included in tab 
        viewportPos (list, optional): Starting viewport pos. Defaults to [2500,2500].
        viewportZoom (int, optional): Initial zoom. Defaults to 1.
        tabColor (_type_, optional): Initial accent color_. Defaults to defaultAccentColor.

    Returns:
        dict: returns a dictionary of tabName, tabID, viewportPos,  viewportZoom, tabColor, and canvasItems
    """
    tab = {
        "tabName": tabName,
        "tabID": tabID,
        "viewportPos": viewportPos,
        "viewportZoom": viewportZoom,
        "tabColor": tabColor,
        "canvasItems": canvasItems
    }
    return tab


def CreateImageData(imagePath, nodeName = "Image_Node"):
    """Create data for a new image

    Args:
        imagePath (_type_): path to the image
        nodeName (str, optional): name of the node. Defaults to "Image_Node".

    Raises:
        Exception: If the path does not exist, it will not create the data.

    Returns:
        dict: returns a dictionary of nodeType, nodeName, nodeID,  creationTime, and imagePath
    """
    if path.exists(imagePath):
        node = {
            "nodeType": "Image_Node",
            "nodeName": nodeName,
            "nodeID": GenerateID(),
            "creationTime": time(),
            "imagePath": imagePath
        }
        return node

    else:
        print("CreateImageNode: Invalid Path")
        raise Exception("CreateImageNode: Invalid Path")

def CreateTextData(text, nodeName = "Text_Node"):
    """Create data for a new Text Item

    Args:
        text (str): text that will be displayed
        nodeName (str, optional): name of the node. Defaults to "Text_Node".

    Returns:
        dict: returns a dictionary of nodeType, nodeName, nodeID,  creationTime, and nodeText
    """
    node = {
        "nodeType": "Text_Node",
        "nodeName": nodeName,
        "nodeID": GenerateID(),
        "creationTime": time(),
        "nodeText": text
    }
    return node