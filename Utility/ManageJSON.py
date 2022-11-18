"""
Description:    This python file is a Utility file that get's data from the JSON database.


Date Created: 9/21/22 
Date Updated: 10/17/22
"""

# Imports
import json
from jsonschema import validate, exceptions
from os import path
from time import time

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from Utility.UtilityFunctions import GenerateID
from Settings.settings import * 

def LoadJSON(fileLocation, createNewProjectOnFail = True):
    """Load the JSON data

    Args:
        fileLocation (str) : Name of the location of the JSON data
        createNewProjectOnFail (bool):    If this is true and the JSON load fails, it will not return a newly created project
    
    Return:
        Returns the data as a Python Object. 
    """
    try:
        with open(fileLocation) as f:
            JSON_Data = json.load(f)
            ValidateJSON(JSON_Data)

            ProjectJSONObject =  JSON_Data["Project"]
            return ProjectJSONObject

    except IOError:                     # Failed to read JSON file
        ConsoleLog.error("JSON Project Read", "Unable to read JSON file in at [" + fileLocation + "]")
        if createNewProjectOnFail:
            ProjectJSONObject = NewProject("Project", 0, [10000, 10000], [CreateTabData("Tab", GenerateID(), [])], [])["Project"]
            return ProjectJSONObject
        else:
            return None
    except exceptions.ValidationError:  # JSON Data formatting is invalid
        ConsoleLog.error("JSON Project Read", "Invalid JSON file at [" + fileLocation + "]")
        if createNewProjectOnFail:
            ProjectJSONObject = NewProject("Project", 0, [10000, 10000], [CreateTabData("Tab", GenerateID(), [])], [])["Project"]
            return ProjectJSONObject
        else:
            return None

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
        "canvasItemID": GenerateID(),
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
            "creationTime": round(time()),
            "canvasItemReferences": [],
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
        "creationTime": round(time()),
        "canvasItemReferences": [],
        "nodeText": text
    }
    return node


def NewProject(projectName, selectedTab, canvasSize, tabs, nodes):
    newJSON = {
        "Project":{
            "projectName": projectName,
            "selectedTab": selectedTab,
            "canvasSize": canvasSize,
            "tabs": tabs,
            "nodes": nodes
        }
    }
    return newJSON

# ----- Save JSON -----
def SaveJSON(JSON_DATA, saveLocation = None):
    newJSON = {
        "Project": JSON_DATA
    }

    if saveLocation != None:
        JSONProjectLocation = saveLocation

    f = open(JSONProjectLocation, "w+")
    f.write(json.dumps(newJSON, indent=4))
    f.close()


# ----- Validate JSON -----
def ValidateJSON(JSON_DATA):
    schema = {
        "type":"object",
        "properties":{           
            "projectName": {"type":"string"},
            "selectedTab": {"type": "number"},
            "canvasSize": {"type": "array"},
            "tabs": {"type": "array"},
            "nodes": {"type": "array"}            
        },
        "required":["projectName","selectedTab","canvasSize","tabs","nodes"]
    }
    projectSchema = {
        "type": "object",
        "properties":{
            "Project":{"type": "object"}
        },
        "required":["Project"]
    }

    validate(JSON_DATA, projectSchema)
    validate(JSON_DATA["Project"], schema)