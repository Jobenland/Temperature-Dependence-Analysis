'''
T E M P E R A T U R E   D E P E N D E N C E   A N A L Y S I S
 This Program is meant to add 7 coulumns with various data from a given set of files
 and add them to a CSV
'''

__author__ = "Jonathan Obenland"
__copyright__ = "Copyright 2019, MEII"
__credits__ = ["Jonathan Obenland","Mikethewatchguy"]
__license__ = "GPL"
__version__ = "2.0.0"
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
import math
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
listOfComb = []
olist = []
nolist = []
tasr = []
acohmic = []
acnonohmic = []
actasr = []
filename =[]
otherthinglist = []
print = sg.EasyPrint

def mainWin():
    form_rows = [
                 [sg.Text("Place all MDATS to include in folder")],
                 [sg.Text('Select new folder', size=(25,1)),sg.InputText(key = 'mdatFolder'),sg.FolderBrowse()],
                 [sg.Checkbox('Frequency Decades', key = ('dec'))],
                 [sg.Button('start'),sg.Exit()]]

    window = sg.Window("Temperature Dependence Version 3")
    event,values = window.Layout(form_rows).Read()

    #start the event listener
    while True:
        if event is None or event == 'Exit':
            break
        if event == 'start':
            files = values['mdatFolder']
            if files =='':
                window.Close()
                sg.PopupError("Insufficent data or Null Pointers given")
                mainWin()
            elif files != '':
                decades = values['dec']
                window.Close()
                print("Symmetrical Cell Converter")
                print("Maryland Energy Innovation Institute -> written by Jonathan Obenland")
                print("System Standby. Awaiting Area Corrected Value...")
                defaultDir = files               
                convertMdatToZip(defaultDir)               
                unzipFiles(defaultDir)
                convertzToTxt(files)
                newZDir = extractedFolder(defaultDir)               
                fileReader(newZDir,decades)
                createMultiX(newZDir,defaultDir)
                generateSheets(newZDir)               
                sg.Popup('Complete')
            break

#converts Z files to TXT files
def convertzToTxt(files):
    pattern = '*.z'
    for (root,dirs,files) in os.walk(files):
        for filename in fnmatch.filter(files,pattern):
            infilename = os.path.join(root,filename)
            oldbase = os.path.splitext(filename)
            newname = infilename.replace('.z', '.txt')
            try:
                output = os.rename(infilename, newname)
            except FileExistsError:
                pass

#generates the combined excel file
#sheet names are stripped to be under 31 chars
def generateSheets(newZDir):
    print('System STANDBY. Awaiting user input')
    csvname = sg.PopupGetText("Enter a name for the combined excel file")
    print('Ready to ammend to ', csvname)
    writer = pd.ExcelWriter(csvname + '.xlsx', engine= 'xlsxwriter')
    for csv in listOfCSV:
        filename, file_extension = os.path.splitext(csv)
        if filename == "Resistance Table.csv":
            print("ignoring system file...")
            break
        print('found ', filename, ' adding to ',csvname) 
        df = pd.read_csv(csv)
        sheetName = filename
        if 'EIS_OCV' in filename:
            sheetName = sheetName.strip('EIS_OCV')
            sheetNameSplit = sheetName.split('_')
            sheetName = sheetNameSplit[0]+sheetNameSplit[1]+sheetNameSplit[2]
        try:      
            df.to_excel(writer, sheet_name=sheetName)
        except xlsxwriter.exceptions.DuplicateWorksheetName:
            print("Duplicate name found, adding DUP to name and ammending...")
            sheetName = sheetNameSplit[0]+sheetNameSplit[1]+sheetNameSplit[2] + "DUP"
            print("duplicate sheet name ",sheetName, " added")
            df.to_excel(writer, sheet_name=sheetName)
    writer.save()

#creates the Resistance Table and the Multi Axis graphing support
#for use with the grapher
def createMultiX(newZDir,defaultDir):
    titleList=[]
    rTable = 'Resistance Table.csv'
    rt = {'Filename':filename,
        'Ohmic': olist,
        'NonOhmic' : nolist,
        'Tasr' : tasr,
        'Area Corrected Ohmic' : acohmic,
        'Area Corrected Non Ohmic' : acnonohmic,
        'Area Corrected Tasr' : actasr}
    dt = pd.DataFrame(data=rt)
    dt.to_csv(rTable,index = False)
    listOfCSV.append(rTable)

    #uncomment this to use Mult X Support
    #VVVVVVVVVVVVVVV
    '''
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
        titleList.append(stringName)

    fileN = "Multi X-Axis Support.csv"
    for i in range(len(listOfComb)):
        if i ==0:
            dataf = {titleList[0] : listOfComb[i]}
            df = pd.DataFrame(data=dataf)
        if i !=0:
            head = titleList[i]
            df[head] = listOfComb[i]
            df.to_csv(fileN, index = False)
            listOfCSV.append(fileN)
    '''
    #^^^^^^^^^^^^^^^

#takes all the z files and places them into one location
def extractedFolder(files):
    newDirName = files
    os.chdir(newDirName)
    #pulling all .z files from the extracted folders into a new folder
    combAll = 'Extracted_Z_Files_And_CSV'
    if not os.path.exists(combAll):
        os.mkdir(combAll)
        print("Directory " , combAll ,  " Created ")
    else:    
        print("Directory " , combAll ,  " already exists")    
    newZDir = newDirName + '/' + combAll
    for root, dirs, files in os.walk((os.path.normpath(newDirName)), topdown=False):
        for name in files:
            if name.endswith('.txt'):
                try:
                    print (name, 'has a z extension. moving to combined folder')
                    SourceFolder = os.path.join(root,name)
                    shutil.copy2(SourceFolder,newZDir)
                except shutil.SameFileError:
                    print(name , " was found with the same file name")       
    return(newZDir)

#Converts the MDATS to ZIPS to be unzipped
def convertMdatToZip(files):
    pattern = '*.mdat'
    for (root,dirs,files) in os.walk(files):
        for filename in fnmatch.filter(files,pattern):
            infilename = os.path.join(root,filename)
            oldbase = os.path.splitext(filename)
            newname = infilename.replace('.mdat', '.zip')
            output = os.rename(infilename, newname)

#Unzips the newly zipped files
def unzipFiles(files):
    pattern = '*.zip'
    for root, dirs, files in os.walk(files):
        for filename in fnmatch.filter(files, pattern):
            print(os.path.join(root,filename))
            zipfile.ZipFile(os.path.join(root,filename)).extractall(os.path.join(root, os.path.splitext(filename)[0]))

#TODO make sure this isnt needed and remove
#THIS is never called
def listOfImpFiles(files):
    fileList = os.listdir(files)
    os.chdir(files)
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

#Reads and does math on the files passed in
def fileReader(impFiles,decades):
    area = sg.PopupGetText("enter area")
    os.chdir(impFiles)
    listF = os.listdir(impFiles)
    i=0
    for file in listF:
        sg.OneLineProgressMeter('File Reader Progress',i,(len(listF)-1),'prgmeter')
        i+=1
        stringFreq = []
        stringTS = []
        stringZPrime = []
        stringZDoublePrime = []
        decFreqIndex = []
        decFreq=[]
        decZP = []
        decZDP = []
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
            if decades==True:
                for val in intFreq:
                    dectest = math.log10(val)
                    try:
                        dosomething = dectest - math.floor(dectest)
                        if dosomething > 0.0 :
                            pass
                        elif dosomething == 0.0:
                            decFreq.append(val)
                            #indexx = intFreq.index(val)
                            decFreqIndex.append(intFreq.index(val))
                    except:
                        print("not a decade")
                for dec in decFreqIndex:
                    decZP.append(zPrimeARC[dec])
                    decZDP.append(zDoublePrimeARC[dec])
                nameoffile, file_extension = os.path.splitext(file)
                datadec = { 'Frequency' : decFreq, 'Z Prime' : decZP, 'Z Double Prime' : decZDP}
                dec = pd.DataFrame(data=datadec)
                fileName = nameoffile +'-Decades.csv'
                dec.to_csv(fileName,index = False)



        olist.append(ohmicZPrime)
        nolist.append(intZPrime[-1]-ohmicZPrime)
        tasr.append(intZPrime[-1])
        acohmic.append(ohmicZPrime*intArea)
        acnonohmic.append((intZPrime[-1]-ohmicZPrime)*intArea)
        actasr.append(intZPrime[-1]*intArea)
        filename.append(file)
        nameoffile, file_extension = os.path.splitext(file)
        comb = [(zPrimeARC[i],positiveZDoublePrime[i]) for i in range(len(zPrimeARC))]
        dataf = { 'Frequency' :intFreq,'Time In Seconds' : intTS, 'Z Prime' : intZPrime, 'Z Double Prime' : intZDoublePrime, 'Z Prime Ohmic Corrected' : zPrimeOC,
        'z Prime Area Corrected' : zPrimeARC, 'Z Double Prime Area Corrected' : zDoublePrimeARC, '+- Z Double Prime' : positiveZDoublePrime, 'DUAL COL' : comb} #column headings for the excel file
        df = pd.DataFrame(data=dataf)
        fileName = nameoffile +'.csv'
        df.to_csv(fileName,index = False)
        listOfCSV.append(fileName)
        listOfComb.append(comb)
        dataDRT = {'Frequency' : intFreq, 'Z Prime Ohmic Corrected' : zPrimeARC, 'Z Double Prime Area Corrected' : zDoublePrimeARC}
        dt = pd.DataFrame(data=dataDRT)
        fileName = nameoffile + 'DRT-Preproccessing.csv'
        dt.to_csv(fileName,index=False,header=None)
        print(file, " has been parsed. continuing to next file...")
        

#Helper function to get the range of the location of the ohmic
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

#Magic Method to call main
if __name__ == '__main__':
    mainWin()
