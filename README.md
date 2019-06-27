![size badge](https://img.shields.io/github/repo-size/Jobenland/Temperature-Dependence-Analysis.svg) ![license](https://img.shields.io/github/license/Jobenland/Temperature-Dependence-Analysis.svg) ![build](https://img.shields.io/badge/Build-Passing-green.svg) ![issues](https://img.shields.io/github/issues/Jobenland/Temperature-Dependence-Analysis.svg) ![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg) ![python](https://img.shields.io/badge/Python-3.x-lightgrey.svg) ![toplang](https://img.shields.io/github/languages/top/Jobenland/Temperature-Dependence-Analysis.svg) ![quality](https://img.shields.io/badge/Code%20Quality-Testing...-red.svg)

## Temperature Dependence Analysis

This Program will extract data from multiple temperature ranges and calculate values such as z prime and z double prime
It will then place the data in a csv that can be used in graphing in the CSV graphing software available for download on my github

NOTE: When given the option to select a zip file, Mac users should instead select the `unzipped folder location` of their original zipped file and leave the final box BLANK. Otherwise, The program will not be able to read the zip file and call a critical error causing the program to crash

## Getting Started and Important Notes
Files MUST be zipped in a folder for correct deployment Ex. `EIS_OCV_..._EXAMPLE.zip`

Also Note, if your files names do not contain a temp value Ex. EIS_OCV_`400` the combination of CSV's will NOT work
  adding a temperature to any position in the filename seperated by a _ is the best way to fix this issue

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Programs and other things needed to run this program
```
Python 3.x
Pip
```

### Installing

A step by step series of examples that tell you how to get a development env running


```
pip install tkinter (not right name) coming soon
pip install pandas 
pip install PySimpleGUI
pip install bokeh
pip install np
```

(optional) not needed

```
import tkinter
import pandas
import PySimpleGUI
import bokeh
```

## Running the tests

To ensure that all modules are loaded and everything is working. Launch the program and attempt give a INT value for the area, a location to save the extracted files, and then the location of the zip file

Given that the user correctly gave a number as the ares, a generic place to put the extracted files, and a ZIP file as the zip path.

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
