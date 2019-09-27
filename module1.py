#-------------------------------------------------------------------------------
# Name:        Generate_Calibration_from_EXCEL_SHEET
# Purpose:
#
# Author:      U560764
#
# Created:     07/06/2019
# Copyright:   (c) U560764 2019
# Licence:     PSA_Licence
#-------------------------------------------------------------------------------
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *
from tkinter.messagebox import * # boîte de dialogue
from tkinter import filedialog
from tkinter import ttk
import re
import os
import shutil
import zipfile
from decimal import *
from pprint import pprint
import openpyxl
from openpyxl import load_workbook
from openpyxl import Workbook
from unidecode import unidecode
import datetime

STATUS_EXCEL_FILE_INPUT       = False
STATUS_OUTPUT_CAL_FILE_PATH = False
STATUS_OUTPUT_CAL_FILE_NAME = False
EXCELFILETYPES = [ ("EXCEL files", "*.xlsm") ]
MAPFILETYPES = [ ("MAP files", "*.map") ]
CFILETYPES = [ ("C files", "*.c") ]
HFILETYPES = [ ("H files", "*.h") ]
CPPFILETYPES = [ ("CPP files", "*.cpp") ]

def deletetype(str1) :
    return str1[0:len(str1)-4]

excel_file_path="C:/Work/DOC/Radars_Calibration_parameters_R5.2.xlsm"
book_CALIB = openpyxl.load_workbook(excel_file_path)
NAME_FRONT_RADAR_SHEET="Front_Radar"
Sheet_Front_Radar_CALIB = book_CALIB.get_sheet_by_name(name = NAME_FRONT_RADAR_SHEET)

LABEL='A'
INIT_VAL='AV'
ARXML_NAME='BH'
INTERFACE_NAME = 'BI'
STRUCT_NAME='BJ'
NB_OF_DIM='AO'
OLD_STRUCT_NAME_CELL=''
for i in range(3,1000) :
    LABEL_CELL=Sheet_Front_Radar_CALIB[LABEL+str(i)].value
    STRUCT_NAME_CELL=Sheet_Front_Radar_CALIB[STRUCT_NAME+str(i)].value
    if (OLD_STRUCT_NAME_CELL != STRUCT_NAME_CELL) and (STRUCT_NAME_CELL is not None   ) :
        #New struct
        print('//declaration of Calibration struct')
        print(STRUCT_NAME_CELL + ' ' + deletetype(STRUCT_NAME_CELL)+';\n')
        OLD_STRUCT_NAME_CELL=STRUCT_NAME_CELL
    ARXML_NAME_CELL=Sheet_Front_Radar_CALIB[ARXML_NAME+str(i)].value
    INIT_VAL_CELL=Sheet_Front_Radar_CALIB[INIT_VAL+str(i)].value
    INTERFACE_NAME_CELL=Sheet_Front_Radar_CALIB[INTERFACE_NAME+str(i)].value
    NB_OF_DIM_CELL=Sheet_Front_Radar_CALIB[NB_OF_DIM+str(i)].value
    if (LABEL_CELL is not None          ) and (STRUCT_NAME_CELL is not None   ) and (ARXML_NAME_CELL is not None    ) and (INIT_VAL_CELL is not None      ) and (INTERFACE_NAME_CELL is not None) and (NB_OF_DIM_CELL is not None     ) :
        if (NB_OF_DIM_CELL ==1 ):
            print(LABEL_CELL+' = '+deletetype(STRUCT_NAME_CELL) + '.'+ARXML_NAME_CELL + ';'+'//init value == '+str(INIT_VAL_CELL)+'\n')
        else :
            #table so loop on table
            print('for (i=0;i<'+str(NB_OF_DIM_CELL-1)+';i++)\n')
            print('{\n')
            print('   '+LABEL_CELL+'[i] = '+deletetype(STRUCT_NAME_CELL) + '.'+ARXML_NAME_CELL+'[i];')
            print('   '+'//init value == '+str(INIT_VAL_CELL)+'\n')
            print('}\n')
