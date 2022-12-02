# Inspire Canvas
Inspire Canvas is a PySide6 application that enables Images, Text, and Files to be placed, scaled, and moved anywhere on the 2D Canvas.

![inspirecanvas](https://i.imgur.com/YEH29Ei.png)


## Installation 
This was only tested on a Windows 10 computer

To develop Inspire Canvas, Python 3.9.5 and all project dependencies will need to be installed on the developer’s computer. Inspire Canvas uses the following Python dependencies:
```
•	PySide6==6.1.2

•	jsonschema==3.2.0

•	Pillow==8.2.0
```
Project Development Setup

1.	Download the project as a ZIP file from the InspireCanvas Repository:
    
    https://github.com/JGerVT/InspireCanvas 

    Extract the files to any location.


2.	Python 3.9.5 is required to develop this software, which can be downloaded and installed here:  

    https://www.python.org/ftp/python/3.9.5/  
    
    Windows 64 bit: https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe
    
    Windows 32 bit: https://www.python.org/ftp/python/3.9.5/python-3.9.5.exe  

    To verify that Python has been installed, open a terminal and type:
    ```
          python --version
    ```
    This should return “Python 3.9.5”.

3.	Next, PIP will need to be set up to install the python dependencies. This is done by typing the following command in a terminal: 
    
    ```
    python -m ensurepip --upgrade
    ```
    
    To verify that PIP has been installed correctly, open a terminal and type:

    ```
    pip --version
    ```


4.	To install all dependencies, the GitHub repository contains a ‘requirements.txt’ file. This file is used to install all project’s dependencies. To install these dependencies, change the directory of the terminal to the Inspire Canvas root folder, then run the command: 

    ```
	pip install -r requirements.txt
    ```

    This will install all required dependencies for the software. 

To run the software, execute the .inspireCanvasMain.py python file.

## Deployment
Once the development setup has been finished, the software can be deployed. To deploy the software, [PyInstaller](https://pyinstaller.org/en/stable/) can be utilized to compile the python script to an executable file (.EXE). To accomplish this, the following steps will need to be taken. 

1.	Install PyInstaller by running the following command:
    ```
    pip install pyinstaller
    ```
2.	Open a terminal and change the directory to Inspire Canvas root folder. Run the following command:
    ```
    pyinstaller --noconfirm --onedir --windowed --name "Inspire Canvas" --icon "Resources/inspireCanvasIcon.png" --add-data "Data;Data/" --add-data "Settings;Settings/" --add-data "Resources;Resources/"  "inspireCanvasMain.py"
    ```
    This command will compile the project to an executable file, located in:
    ```
  	/dist/Inspire Canvas/Inspire Canvas.exe
    ```
	
Once these steps have been followed, the python project has successfully been deployed. 

