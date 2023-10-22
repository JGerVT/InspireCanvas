# Inspire Canvas
Inspire Canvas is a PySide6-based application featuring a minimal graphical user interface that empowers users to effortlessly arrange, resize, and reposition Images, Text, and Files on a two-dimensional canvas.

![inspirecanvas](https://i.imgur.com/YEH29Ei.png)

```* This was only tested on a Windows 10 64bit computer *```

## Requirements
To develop Inspire Canvas, [Python 3.9.5](https://www.python.org/ftp/python/3.9.5/) and all project dependencies will need to be installed. 

Inspire Canvas uses the following Python dependencies:
- [PySide6==6.1.2](https://pypi.org/project/PySide6/6.1.2/)
- [jsonschema==3.2.0](https://pypi.org/project/jsonschema/3.2.0/)

## Developer Instructions 

1.	[Download or Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) the Inspire Canvas Repository.

2.	Download and install [Python 3.9.5](https://www.python.org/ftp/python/3.9.5/):  
    
    - Windows 64 bit: https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe
    - Windows 32 bit: https://www.python.org/ftp/python/3.9.5/python-3.9.5.exe  

    **Verify that the correct version of Python has been installed by typing the following command in a terminal:**
	```
	python --version
	```

3.	Install PIP 

	PIP is required to install the python dependencies. This can be done with the following command:
    
    ```
    python -m ensurepip --upgrade
    ```
  
4.	Install all dependencies. 

	There are two required dependencies for this project. To install these dependencies, change the directory of the terminal to the Inspire Canvas root folder, then run the following command: 

	```
	pip install PySide6==6.1.2
	```
	```
	pip install jsonschema==3.2.0
	```
	
5. 	Execute the .inspireCanvasMain.py python file.

## Deployment
Once the development setup has been finished, the software can be deployed as an executable file. To deploy the software, [PyInstaller](https://pyinstaller.org/en/stable/) can be utilized to compile the python script to an executable file (.EXE). The GitHub repository includes a ‘Inspire Canvas.spec’ file, which is used to tell PyInstaller how to compile the source code. 

### Deploy Inspire Canvas

1.	Install PyInstaller by running the following command:
    ```
    pip install pyinstaller
    ```
2.	Open a terminal and change the directory to Inspire Canvas root folder. Run the following command:
    ```
    pyinstaller "Inspire Canvas.spec"
    ```
    This command will compile the project as an executable file, located in 
    
    ```/dist/Inspire Canvas/Inspire Canvas.exe```
    
**Once these steps have been completed, the python project has successfully been deployed.**

## Folder Structure
```
Inspire Canvas/
| - Data/               // - Contains the softwareLog.log file for logging program actions
| - Resources/		// - Where .svg icons and the software icon are stored.
| - Settings/           // - Where global settings are stored, in “settings.py”. 
| - Utility/            // - Contains various utility python scripts that are utilized globally throughout my application. 
| - UIComponents/	// - Contains python code for GUI elements / PySide QWidgets.
| | - Canvas/           // - Contains all GUI elements for the canvas
| | | - CanvasItem      // - Contains all GUI python files for Canvas Items on the canvas.
| | | - CanvasUtility	// - Contains utility python classes for grouping together canvas items and selecting canvas items.
| | - ContextMenu/      // - Contains GUI elements for the context menu on right click.
| | - TopBar/     	// - Contains all GUI elements for the software’s Tab Bar.
| - Inspire Canvas.spec // - PyInstaller installation settings
| - inspireCanvasMain.py// - Main python file to run the program.

```
