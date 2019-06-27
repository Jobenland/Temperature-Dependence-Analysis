#!/usr/bin/env python
'''
T E M P E R A T U R E   D E P E N D E N C E   A N A L Y S I S
 This Program is meant to add 7 coulumns with various data from a given set of files
 and add them to a CSV
'''

__author__ = "Jonathan Obenland"
__copyright__ = "Copyright 2019, MEII"
__credits__ = ["Jonathan Obenland","Mikethewatchguy"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jonathan Obenland"
__email__ = "jobenland1@gmail.com"
__status__ = "Production"


#all imports
#TODO clean this up it looks terrible
import sys
import tkinter
from tkinter import ttk
import abc
import os
import csv
import os, sys
import numpy as np
import pandas as pd
import pandas
import glob as gb
import glob 
import datetime, time
import itertools as itls
import time
from zipfile import ZipFile
import xlsxwriter
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
import fnmatch
import zipfile
import shutil
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg

arrayOfImpFiles = []
impedanceElectrodeASRList = []
impedanceTotalASRList = []
impedanceOhmicList = []
impedanceTimeInSecounds = []
impedanceTimeInHours = []
listOfCSV = []

#Main Winodw that displays starting data
def mainWin():
    form_rows = [[sg.Text("Enter the file name, file path to save, and the location of the files")],
                 [sg.Text('Enter the the area', size=(21,1)),sg.InputText(key = 'area')],
                 [sg.Text('Enter the location to save', size=(25,1)),sg.InputText(key = 'files'),sg.FolderBrowse()],
                 [sg.Text('Enter the location of the .zip', size=(25,1)),sg.InputText(key = 'zip'),sg.FileBrowse()],
                 [sg.Button('start'),sg.Exit()]]

    window = sg.Window("added columns program")
    event,values = window.Layout(form_rows).Read()
    #start the event listener
    while True:

        if event is None or event == 'Exit':

            break

        if event == 'start':
            area = values['area']
            directory = values['files']
            zipp = values['zip']

            try:
                intTemp = (float(area))
                os.chdir(directory)
            except ValueError:
                window.Close()
                sg.PopupError("Ensure you Have entered a vaid number")
                mainWin()   
            except FileNotFoundError:
                window.Close()
                sg.PopupError("The OS could not detect that directory or ZIP file")
                mainWin()

            if area == '' or directory == '':
                window.Close()
                sg.PopupError("Insufficent data or Null Pointers given")
                mainWin()
            
            #if both areas are populated then
            if area != '' and directory != '' and zipp != '':
                ntUZ = True
                window.Close()
                zDir = unzipper(directory,zipp,ntUZ)
                testing(area,zDir)
                generateSheets(listOfCSV,'Combined CSV')
                sg.Popup("complete")
                mainWin()
                #impedanceReader(area,directory)
            if area != '' and directory != '' and zipp == '':
                ntUZ = False
                window.Close()
                zDir = unzipper(directory,zipp,ntUZ)
                testing(area,zDir)
                generateSheets(listOfCSV,'Combined CSV')
                sg.Popup("complete")
                mainWin()

#Linear definition to create folder
#navigate to folder, extract all the data into another folder
#move all .z files to a new folder
#create CSV's there
def unzipper(directory,zipp,ntUZ):
    os.chdir(directory)
    newDirName = directory
    
        #outfile = open(output,'w')
    if ntUZ == True:
    #create new folder to put extracted data in
        
        newFolder = sg.PopupGetText('Enter a name for the new folder', directory)
        try:
            if not os.path.exists(newFolder):
                os.makedirs(newFolder)
        except OSError:
            print('Error')

        #extract all data to the new folder
        newDirName = directory + '/' + newFolder
        
        os.chdir(newDirName)
        with ZipFile(zipp,'r') as zipObj:
            zipObj.extractall(newDirName)
        pattern = '*.mdat'
        for (root,dirs,files) in os.walk(newDirName):
            for filename in fnmatch.filter(files,pattern):
                infilename = os.path.join(root,filename)
                oldbase = os.path.splitext(filename)
                newname = infilename.replace('.mdat', '.zip')
                output = os.rename(infilename, newname)
    if ntUZ == False:
        for filename in os.listdir(directory):
            infilename = os.path.join(directory,filename)
            if not os.path.isfile(infilename): continue
            oldbase = os.path.splitext(filename)
            newname = infilename.replace('.mdat', '.zip')
            output = os.rename(infilename, newname)

        
    
    #walk the OS path of all the folders and find all .zip files
    #extract everything it finds
    pattern = '*.zip'
    for root, dirs, files in os.walk(newDirName):
        for filename in fnmatch.filter(files, pattern):
            print(os.path.join(root,filename))
            zipfile.ZipFile(os.path.join(root,filename)).extractall(os.path.join(root, os.path.splitext(filename)[0]))
    
    #pulling all .z files from the extracted folders into a new folder
    combAll = 'Extracted_Z_Files_And_CSV'
    try:
        if not os.path.exists(combAll):
            os.makedirs(combAll)
    except OSError:
        print('Error')
    try:
        newZDir = newDirName + '/' + combAll
        for root, dirs, files in os.walk((os.path.normpath(newDirName)), topdown=False):
            for name in files:
                if name.endswith('.z'):
                    print ('Found')
                    SourceFolder = os.path.join(root,name)
                    shutil.copy2(SourceFolder,newZDir)
    except shutil.SameFileError:
        print("Same File Name Found")
    return(newZDir)

#Definiton to do that math on the .z files in the new folder
def testing(area,directory):
    

    #error checking to make sure no rouge non-Impedance Files got in
    impFiles = listOfImpFiles(area,directory)
    os.chdir(directory)

    for file in impFiles:
        stringFreq = []
        stringTS = []
        stringZPrime = []
        stringZDoublePrime = []

        with open (file, 'r', encoding = 'ISO-8859-1') as f:
            for row in f:
                if 'End Header:' in row:
                    for x in f:
                        stringFreq.append(x.split('\t')[0])
                        stringTS.append(x.split('\t')[3])
                        stringZPrime.append(x.split('\t')[4])
                        stringZDoublePrime.append(x.split('\t')[5])
                    intFreq = [float(i) for i in stringFreq]
                    intTS = [float(i) for i in stringTS]
                    intZPrime = [float(i) for i in stringZPrime]
                    intZDoublePrime = [float(i) for i in stringZDoublePrime]
                    #calls the function to calculate the range of the values
                    #needed to find the ohmin
                    startRange,endRange = getRange(intZDoublePrime)
                    #-1 is the "error code" used when data never goes below the x-axis
                    if endRange == -1:
                        zDoublePrimeShort = max(intZDoublePrime)
                        zDoublePrimeABS = zDoublePrimeShort
                        ohmicZDoublePrime = zDoublePrimeShort
                    elif endRange > 0:
                        intStart = int(startRange)
                        intEnd = int(endRange)
                        zDoublePrimeShort = intZDoublePrime[intStart:intEnd]
                        zDoublePrimeABS= [abs(i) for i in zDoublePrimeShort]
                        ohmicZDoublePrime = min(zDoublePrimeABS)
            intArea = (float(area))
            if ohmicZDoublePrime in intZDoublePrime:
                ohmicZPrimeIndex = intZDoublePrime.index(ohmicZDoublePrime)
                ohmicZPrime = intZPrime[ohmicZPrimeIndex]
            else:
                ohmicZPrimeIndex = intZDoublePrime.index(-ohmicZDoublePrime)
                ohmicZPrime = intZPrime[ohmicZPrimeIndex]
            zPrimeOC = [((intZPrime[i])-(ohmicZPrime)) for i in range(len(intZPrime))]
            zPrimeARC= [((zPrimeOC[i])*(intArea)) for i in range(len(intZPrime))]
            zDoublePrimeARC = [((intZDoublePrime[i])*(intArea)) for i in range(len(intZDoublePrime))]
            positiveZDoublePrime = [-x for x in zDoublePrimeARC]
        createCSV(file,directory,intTS, intFreq, intZPrime,intZDoublePrime,zPrimeOC,zPrimeARC,zDoublePrimeARC,positiveZDoublePrime)
        print("rp?")

#definition to get the range of the data
#will get the last negative point and the last positive point
#if neither exist return "error codes"
def getRange(intZDoublePrime):
    PG=[]
    NG=[]
    t=0
    #first part tests point and the next point
    #to find positive then negative
    for i in range(len(intZDoublePrime)):
        if intZDoublePrime[i] > 0:
            t+1
        elif intZDoublePrime[i] < 0:
            if intZDoublePrime[i-1] >0:
                indexx = i-1
                break
    
    #makes lists for all the positive corresponding index
    #makes lists for all the negative corresponding index
    for i in range(len(intZDoublePrime)):
        if intZDoublePrime[i] < 0:
            PG.append(i)
        elif intZDoublePrime[i] > 0:
            NG.append(i)
        elif intZDoublePrime[i] == 0:
            OH = intZDoublePrime[i]
            break
   
   #checking to make sure that the graph has both
   #positive and negative values
    if NG == [] and PG != []:
        startRange = min(intZDoublePrime)
        endRange = -1
    if NG != [] and PG != []:
        j = (len(NG))
        startRange = indexx
        endRange = startRange + 1
    return(startRange,endRange)

#creates the CSV's and appends them to a list for later
# excel use   
def createCSV (file,directory,intTS, intFreq, intZPrime,intZDoublePrime,zPrimeOC,zPrimeARC,zDoublePrimeARC,positiveZDoublePrime):
    dirpath = os.chdir(directory)
    fileN = file +'.csv'
    dataf = { 'Frequency' :intFreq,'Time In Secounds' : intTS, 'Z Prime' : intZPrime, 'Z Double Prime' : intZDoublePrime, 'Z Prime Ohmic Corrected' : zPrimeOC,
        'z Prime Area Corrected' : zPrimeARC, 'Z Double Prime Area Corrected' : zDoublePrimeARC, '+- Z Double Prime' : positiveZDoublePrime } #column headings for the excel file
    df = pd.DataFrame(data=dataf)
    df.to_csv(fileN,index = False)
    listOfCSV.append(fileN)

#definition to make an array of Files that are the experiment "Impedance"
def listOfImpFiles(area,directory):
    os.chdir(directory)
    fileList = os.listdir(directory)
    global listOfImpFiles
    for file in fileList:

        with open(file, "r", encoding = 'ISO-8859-1') as f:

            for row in f:

                if 'Exp Name:' in row:
                    strippedExperimentName = row.strip('Exp Name: \n')
                    if strippedExperimentName == 'Impedanc':
                        for row in f:
                            if 'End Information' in row:
                                strippedImpedanceType = row.strip('End Information: \n')
                                if strippedImpedanceType == 'AC File Columns':
                                    arrayOfImpFiles.append(file)
    return arrayOfImpFiles

#gets the time in the file
def getTime(file):
    with open(file,'r',encoding = "ISO-8859-1") as f:
        for row in f:
            if 'Time:' in row:
                strippedTime= row.strip('Time: \n')
                return strippedTime
                
#gets the date in the file
def getDate(file):
    with open(file,'r',encoding = "ISO-8859-1") as f:
        for row in f:
            if 'Date:' in row:
                strippedDate= row.strip('Date: \n')
                return strippedDate

#definition to generate a EXCEL file
# with multiple sheet names as all the .z files from
# different temperatures
def generateSheets(listOfCSV, fileName):
    fileName = sg.PopupGetText("enter a name for the combined Excel file", 'Excel File Name')
    writer = pd.ExcelWriter(fileName+'.xlsx', engine = 'xlsxwriter') 
    for csv in listOfCSV:
        csvSplitList = csv.split('_')
        print(csvSplitList)
        for val in csvSplitList:
            try:
                if val != 'aging' or val != 'preaging':
                    
                    intTemp = (int(val))
            except ValueError:
                print ('Was Not a Temp')
        stringName=(str(intTemp))
        df = pd.read_csv(csv)
        df.to_excel(writer, sheet_name=stringName)
    writer.save() 

#magic method to call main           
if __name__ == '__main__':
    mainWin()