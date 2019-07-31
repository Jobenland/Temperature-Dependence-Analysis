![size badge](https://img.shields.io/github/repo-size/Jobenland/Temperature-Dependence-Analysis.svg) ![license](https://img.shields.io/github/license/Jobenland/Temperature-Dependence-Analysis.svg) ![build](https://img.shields.io/badge/Build-Passing-green.svg) ![issues](https://img.shields.io/github/issues/Jobenland/Temperature-Dependence-Analysis.svg) ![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg) ![python](https://img.shields.io/badge/Python-3.x-lightgrey.svg) ![toplang](https://img.shields.io/github/languages/top/Jobenland/Temperature-Dependence-Analysis.svg) ![quality](https://img.shields.io/badge/Code%20Quality-Testing...-red.svg)

## Temperature Dependence Analysis

This Program will extract data from multiple temperature ranges and calculate values such as z prime and z double prime
It will then place the data in a csv that can be used in graphing in the CSV graphing software available for download on my github

NOTE: When given the option to select a zip file, Mac users should instead select the `unzipped folder location` of their original zipped file and leave the final box BLANK. Otherwise, The program will not be able to read the zip file and call a critical error causing the program to crash(working on a fix in the future)

UPDATE: To use the New windows for both MAC and Windows make sure to clone version 2.0 and run `TDV2.py`

## Getting Started and Important Notes
NOTE: Please see Images below for information regarding the correct files to give the program

Files MUST be zipped in a folder for correct deployment Ex. `EIS_OCV_..._EXAMPLE.zip` this is NOT needed in `TDV2.py`

On startup, the user will be prompted for a folder of MDAT Files. this program can handle MDATS, ZIPPED folders, and UNZIPPED folders.
each file in the folder should be a Temperature for a specific material. For example `EIS_OCV_500_DRT_1pCO2.zip` or `EIS_OCV_500_DRT_1pCO2.mdat` would be given that contains .mpro, .cor, and .z files. see images below for more information.

Once You have successfully put all your files in a folder and selected `start` on the main window the program is ready to analyze the data

### Prerequisites

Programs and other things needed to run this program
```
Python 3.x
Pip
```

### Installing

A step by step series of examples that tell you how to get a development env running

Automatic Method

`pip install -r requirements.txt`

Manual Method
```
pip install pandas 
pip install PySimpleGUI
pip install bokeh
pip install np
```

## Running the program

#cloning the directory and preparing for executuion
the best way to install and run the program is to clone this repo to your home directory by typing `git clone https://github.com/Jobenland/Temperature-Dependence-Analysis`. Once the directory has been cloned, change the directory `cd Temperature-Dependence-Analysis` to the directory of the repository. Ensure you are in the directory by typing `dir` and checking the output for a file called `TCPV3`. Type `python --version` or `python3 -version` and ensure the output version is at least 3.x.

## Deployment

The best way to deploy this software for use in lab is to run locally either through command prompt or a Python Interpreter of your own
## Built With

* [Pandas](https://pandas.pydata.org/) - Used to edit and read CSV's
* [PySimpleGUI](https://pypi.org/project/PySimpleGUI/) - Used to create a GUI more efficiently
* [TKinter](https://docs.python.org/3/library/tkinter.html) - Used as backend GUI framework and support
* [Bokeh](https://bokeh.pydata.org/en/latest/) - Used as plotting software for the plot function
* [NP](http://cs231n.github.io/python-numpy-tutorial/) - Help with scientific calculations

## Contributing

If any Enhancements, Features or Problems arrise, Please submit a request on github

## Versioning

No versioning control has been set up yet but I am working on having this work in the Future 

## Authors

* **Jonathan Obenland** - *Initial work* - [Jonathan Obenland](https://github.com/jobenland)

## License

This project is licensed under the GPL License
