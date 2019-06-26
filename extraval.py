#!/usr/bin/env python
'''
VERSION 2.0 - OPTIMIZED

 This Program is meant to add 7 coulumns with various data from a given set of files
'''

__author__ = "Jonathan Obenland"
__copyright__ = "Copyright 2019, MEII"
__credits__ = ["Jonathan Obenland", "Ian Robinson", "Mikethewatchguy"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jonathan Obenland"
__email__ = "jobenland1@gmail.com"
__status__ = "Production"


#all imports
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


#checks to ensure that version is up to date
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg

#Creation of the array
#each experiment has its own array
#dynamic = galvanodynamics
#static = galvanostatic
#impedance = impedance AC (not DC)

arrayOfImpFiles = []
impedanceElectrodeASRList = []
impedanceTotalASRList = []
impedanceOhmicList = []
impedanceTimeInSecounds = []
impedanceTimeInHours = []
listOfCSV = []
def mainWin():
    form_rows = [[sg.Text("Enter the file name, file path to save, and the location of the files")],
                 [sg.Text('Enter the the area', size=(21,1)),sg.InputText(key = 'area')],
                 [sg.Text('Enter the location to save', size=(25,1)),sg.InputText(key = 'files'),sg.FolderBrowse()],
                 [sg.Text('Enter the location of the .zip', size=(25,1)),sg.InputText(key = 'zip'),sg.FileBrowse()],
                 [sg.Button('start'),sg.Exit()]]

    window = sg.Window("added columns program")

    event,values = window.Layout(form_rows).Read()

    while True:

        if event is None or event == 'Exit':
            break
        if event == 'start':
            area = values['area']
            directory = values['files']
            zipp = values['zip']

            if area == '' or directory == '':
                window.Close()
                sg.Popup("ERROR: Insufficent data or Null Pointers given")
                mainWin()
            if area != '' or directory != '':
                window.Close()
                zDir = unzipper(directory,zipp)
                testing(area,zDir)
                generateSheets(listOfCSV,'Combined CSV')
                sg.Popup("complete")
                mainWin()
                #impedanceReader(area,directory)
def unzipper(directory,zipp):

    os.chdir(directory)
    newFolder = 'Extracted'
    try:
        if not os.path.exists(newFolder):
            os.makedirs(newFolder)
    except OSError:
        print('Error')


    newDirName = directory + '/' + newFolder
    os.chdir(newDirName)
    with ZipFile(zipp,'r') as zipObj:
        zipObj.extractall(newDirName)
    
    pattern = '*.zip'
    for root, dirs, files in os.walk(newDirName):
        for filename in fnmatch.filter(files, pattern):
            print(os.path.join(root,filename))
            zipfile.ZipFile(os.path.join(root,filename)).extractall(os.path.join(root, os.path.splitext(filename)[0]))
    
    combAll = 'Extracted Z Files'
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

def impedanceReader(area, directory):

    stringZPrime,stringZDoublePrime,dateTimeList,floatTime = ([]for i in range(4))
    stringFreq=[]
    stringTS = []
    impedanceFileCount=0
    global impedanceElectrodeASRList
    global impedanceTotalASRList
    global impedanceOhmicList
    global impedanceTimeInSecounds
    global impedanceTimeInHours
    global arrayOfImpFiles

    impFiles = listOfImpFiles(area,directory)
    os.chdir(directory)
    for file in impFiles:

        with open(file, 'r') as f:

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
                    intzDoublePrime = [float(i) for i in stringZDoublePrime]
                    zDoublePrimeShort = intzDoublePrime[5:25]
                    zDoublePrimeABS = [abs(i) for i in zDoublePrimeShort]
            ohmicZDoublePrime = min(zDoublePrimeABS)
            ohmicZPrime = min(z)
            if ohmicZDoublePrime in intzDoublePrime:
                ohmicZPrimeIndex = intzDoublePrime.index(ohmicZDoublePrime)
                ohmicZPrime = intZPrime[ohmicZPrimeIndex]
            else:
                ohmicZPrime = intzDoublePrime.index(-ohmicZDoublePrime)

            #ammending things and setting things   
            ohmicMin = intZPrime[ohmicZPrimeIndex]
            totalASR = max(intZPrime[ohmicZPrimeIndex:])
            electrodeASR = totalASR-ohmicMin
            impedanceElectrodeASRList.append(electrodeASR)
            impedanceTotalASRList.append(totalASR) 
            impedanceOhmicList.append(ohmicMin)
            timeT = getTime(file)
            dateD = getDate(file)
            dateTimeString = dateD + ' ' + timeT
            dateTimeFormat = datetime.datetime.strptime(dateTimeString, '%d/%m/%Y %I:%M:%S %p')
            dateTimeList.append(dateTimeFormat)
            correctedTime = time.mktime(dateTimeFormat.timetuple())
            floatTime.append(float(correctedTime))
            impedanceTimeInSecounds.append(correctedTime)
            minTime = min(impedanceTimeInSecounds)
            impedanceTimeInHours = [((impedanceTimeInSecounds[i]-minTime)/3600) for i in range(len(impedanceTimeInSecounds))]
            intArea = (float(area))

            
            #ohmicARC = ((ohmicZPrime)*(intArea))

            
            impedanceZPrimeOC = [((intZPrime[i])-(ohmicZPrime)) for i in range(len(intZPrime))]
            impedanceZPrimeARC= [((impedanceZPrimeOC[i])*(intArea)) for i in range(len(intZPrime))]
            impedanceZDoublePrimeARC = [((intzDoublePrime[i])*(intArea)) for i in range(len(intzDoublePrime))]
            #impedanceZPrimeOhmicOC = [((impedanceZPrimeOC[i])*(intArea)) for i in range(len(impedanceZPrimeOC))]


            print("stop")

    print(len(impedanceTimeInSecounds))

    print(len(impedanceZDoublePrimeARC))
    print(len(impedanceZPrimeARC))
    print(len(impedanceZPrimeOC))
    
    print(len(impedanceOhmicList))
    print(len(impedanceElectrodeASRList))

    createCSV(directory,intFreq,impedanceElectrodeASRList,impedanceOhmicList,impedanceTotalASRList,impedanceZPrimeOC,impedanceZPrimeARC,impedanceZDoublePrimeARC)

            #impedanceZPrimeOC=[((impedanceZPrimeARC[i])-(ohmicZPrime[i])) for i in range(len(impedanceZPrimeARC))]
            #print (impedanceZPrimeOC)


def testing(area,directory):
    stringFreq = []
    stringTS = []
    stringZPrime = []
    stringZDoublePrime = []

    impFiles = listOfImpFiles(area,directory)
    os.chdir(directory)

    for file in impFiles:
        with open (file, 'r') as f:
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
                    startRange,endRange = getRange(intZDoublePrime)
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

            



def getRange(intZDoublePrime):
    PG=[]
    NG=[]
    t=0
    for i in range(len(intZDoublePrime)):
        if intZDoublePrime[i] > 0:
            t+1
        elif intZDoublePrime[i] < 0:
            if intZDoublePrime[i-1] >0:
                indexx = i-1
                #for j in range(i):
                    #del intZDoublePrime[j]
                break
    
    
    for i in range(len(intZDoublePrime)):
        if intZDoublePrime[i] < 0:
            PG.append(i)
        elif intZDoublePrime[i] > 0:
            NG.append(i)
        elif intZDoublePrime[i] == 0:
            OH = intZDoublePrime[i]
            break
    
    if NG == [] and PG != []:
        startRange = min(intZDoublePrime)
        endRange = -1
    if NG != [] and PG != []:
        j = (len(NG))
        startRange = indexx
        endRange = startRange + 1
    return(startRange,endRange)



                    



    
def createCSV (file,directory,intTS, intFreq, intZPrime,intZDoublePrime,zPrimeOC,zPrimeARC,zDoublePrimeARC,positiveZDoublePrime):
    dirpath = os.chdir(directory)
    fileN = file +'.csv'
    dataf = { 'Frequency' :intFreq,'Time In Secounds' : intTS, 'Z Prime' : intZPrime, 'Z Double Prime' : intZDoublePrime, 'Z Prime Ohmic Corrected' : zPrimeOC,
        'z Prime Area Corrected' : zPrimeARC, 'Z Double Prime Area Corrected' : zDoublePrimeARC, '+- Z Double Prime' : positiveZDoublePrime } #column headings for the excel file
    df = pd.DataFrame(data=dataf)
    df.to_csv(fileN,index = False)
    listOfCSV.append(fileN)
    #writer = pd.ExcelWriter('yourfile.xlsx', engine='xlsxwriter')
    #df = pd.read_csv(fileN)
    #df.to_excel(writer, sheet_name='Impedance')
    #writer.save()
    #listofCSV.append(fileN)


def listOfImpFiles(area,directory):
    os.chdir(directory)
    fileList = os.listdir(directory)
    global listOfImpFiles
    for file in fileList:

        with open(file, "r") as f:

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

def generateSheets(listOfCSV, fileName):
    writer = pd.ExcelWriter(fileName+'.xlsx', engine = 'xlsxwriter')
    
    for csv in listOfCSV:
        csvSplitList = csv.split('_')
        print(csvSplitList)
        for val in csvSplitList:
            try:
                intTemp = (int(val))
            except ValueError:
                print ('Was Not a Temp')
        stringName=(str(intTemp))
        df = pd.read_csv(csv)
        df.to_excel(writer, sheet_name=stringName)
    writer.save() 
                    

            
if __name__ == '__main__':
    mainWin()