# Inspire Canvas
Inspire Canvas is a PySide6 application with a minimal GUI that enables Images, Text, and Files to be placed, scaled, and moved anywhere on a 2D Canvas.

![inspirecanvas](https://i.imgur.com/YEH29Ei.png)

```* This was only tested on a Windows 10 64bit computer *```

## Developer Instructions 

To develop Inspire Canvas, Python 3.9.5 and all project dependencies will need to be installed. 

Inspire Canvas uses the following Python dependencies:
```
- PySide6==6.1.2
- jsonschema==3.2.0
```
### Project Development Setup

1.	[Download or Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) the Inspire Canvas Repository.

2.	Download and install [Python 3.9.5](https://www.python.org/ftp/python/3.9.5/):  
    
    - Windows 64 bit: https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe
    - Windows 32 bit: https://www.python.org/ftp/python/3.9.5/python-3.9.5.exe  

    **Verify that the correct version of Python has been installed by typing the following command in a terminal:**
	```
	python --version
	```
    This should return “Python 3.9.5”

3.	Install PIP 

	PIP is required to install the python dependencies. This can be done with the following command:
    
    ```
    python -m ensurepip --upgrade
    ```
    
    **Verify that PIP has been installed correctly, open a terminal and type:**

    ```
    pip --version
    ```


4.	Install all dependencies. 

	
	The Github repository contains a ‘requirements.txt’ file. This file is used to install all project’s dependencies. 
	
	To install these dependencies, change the directory of the terminal to the Inspire Canvas root folder, then run the following command: 

	```
	install -r requirements.txt
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
    This command will compile the project as an executable file, located in ```/dist/Inspire Canvas/Inspire Canvas.exe```
    
**Once these steps have been completed, the python project has successfully been deployed.**