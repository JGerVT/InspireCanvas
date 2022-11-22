""" 
Description:    This python file provides the functionality for FileCanvasItems on the Canvas

Date Created: 11/21/22 
Date Updated: 11/22/22
"""

#Imports
import os

#Components Used:
from UI_Components.Canvas.CanvasItem.baseCanvasItem import *  

class FileCanvasItem(CanvasItem):
    def __init__(self, parent, canvasItemData) -> None:
        """ Provides the functionality for File Canvas Items

        Args:
            canvasItemData (dict): CanvasItem data that is parsed and applied to the canvas item. 
        """
        super().__init__(parent, canvasItemData)


        # Set Attributes
        self.SetRect(QRectF(QPointF(self.itemPos.x(),self.itemPos.y()), QSize(300, 75)))

        # NodeData
        self.filePath = self.nodeData["filePath"]

        # Properties
        self.fileName = self.GetFileName(self.filePath)
        self.fileIcon = self.GetFileIcon(self.fileName).pixmap(QSize(50,50),QIcon.Normal,QIcon.On)

        # Icon
        self.icon = QGraphicsPixmapItem(self)
        self.scaled = QPixmap(self.fileIcon).scaled(50,50,Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.icon.setPixmap(self.scaled)
        self.icon.setPos(12, self.boundingRect().height()/2 - self.icon.boundingRect().height()/2)


    def paint(self, painter, option, widget) -> None:
        painter.setRenderHint(painter.Antialiasing, True)

        painter.save()

        # Draw Background
        painter.setBrush(QBrush("black"))
        painter.drawRoundedRect(self.boundingRect(), 5,5)


        # Draw Text
        font = painter.font()
        font.setPointSize(9)
        painter.setFont(font)

        painter.setPen(QPen("White"))
        painter.drawText(QRect(72,0, self.boundingRect().width() - 80 - 12, self.boundingRect().height()), Qt.AlignmentFlag.AlignVCenter, self.fileName)


        painter.restore()
        return super().paint(painter, option, widget)

    def GetFileIcon(self, filePath) -> QIcon:
        """Function that gets the icon from a filepath.

        Args:
            filePath (_type_): _description_

        Returns:
            QIcon: _description_
        """
        try:
            fileInfo = QFileInfo(filePath)
            iconProvider = QFileIconProvider()
            icon = iconProvider.icon(fileInfo)
            return icon
        except:
            ConsoleLog.error("Unable to access File Icon", str(filePath) + " - This path does not have a valid icon.")
            self.deleteLater()
            return None        

    def GetFileName(self, filePath):
        """ Get name of file from filePath

        Args:
            filePath (str): path to the file

        Returns:
            str: Returns the file name, including it's extension. 

        Example:
            Input:  E:\TestFiles\example.txt
            Return: example.txt
        """
        return os.path.basename(filePath)