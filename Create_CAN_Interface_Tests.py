#######################################################
# PSA
# date: 18/01/2019
# username:
# name: YJE
# description: CAN test interfaces
#######################################################
#!/usr/bin/env python

#import Libs
#import urllib.request as urllib2
#import openpyxl
import os
import glob
import Def_Create_Test_CAN
import cantools
import canmatrix
import canmatrix.convert as convert
from openpyxl import Workbook
from lxml import etree
######################################################

#From DOCINFO download the file Data_Conversion_Form_R5.xlsx

    

Relase_Version                        ="5.0.8"
Relase_Version_MAJOR_ID               =Relase_Version.split(".")[0]
Relase_Version_MIDDLE_ID              =Relase_Version.split(".")[1]
Relase_Version_MINOR_ID               =Relase_Version.split(".")[2]
CAN_INTERFACE                         = []
CPP_FILES                             = []
SIG_INTERFACE                         = []
SIG_INTERFACE_NOT_FOUND               = []
SVN_PATH                              = "C:\\ADAS\\ec400"
DEV_PATH                              = "\\Development\\PrjHAD"
INTEG_PATH                            = "\\SWIntegration"
SOURCE_PATH                           = "\\PSA_Component_Sources\\Customer"
SOURCE_FILE_PATH                      = SVN_PATH + DEV_PATH + INTEG_PATH + "\\Release"+Relase_Version_MAJOR_ID + "\\Release"+Relase_Version + SOURCE_PATH
CAN_DBC_PATH                          = "\\CANAlyzer\\DB\\"
CAN_DBC_NAME                          = "Matrice_FRONT_RADAR_GEN5_FIXED_R5.0_V2"
CAN_DBC_DIR                           = SVN_PATH + DEV_PATH + INTEG_PATH + "\\Release"+Relase_Version_MAJOR_ID + "\\Release"+Relase_Version + CAN_DBC_PATH
CAN_DBC_FILE                          = CAN_DBC_DIR + CAN_DBC_NAME + ".dbc"
XML_DBC_FILE                          = CAN_DBC_DIR + CAN_DBC_NAME + ".xml"
SCRIPT_DIR                            = "C:\\Work\\Script\\"
EXCEL_TEST_FILE_NAME                  = SCRIPT_DIR + "STPR.xlsx"

print(CAN_DBC_FILE)

#call function
CPP_FILES                             = Def_Create_Test_CAN.GET_CPP_FILES(SOURCE_FILE_PATH,".cpp")
CAN_INTERFACE                         = Def_Create_Test_CAN.Read_XLSX_FILE("C:\\Work\\Script\\Copie de Data_Conversion_Form_R5.xlsx")
#create file XLSX

EXCEL_TEST_FILE                       =  Workbook() #open (EXCEL_TEST_FILE , 'w')
EXCEL_TEST_FILE_WORK_SHEET            = EXCEL_TEST_FILE.active
EXCEL_TEST_FILE_WORK_SHEET.title       = "Can Communication tests"

#add head
Def_Create_Test_CAN.Write_Head_EXCEL_File(EXCEL_TEST_FILE_WORK_SHEET)
EXCEL_TEST_FILE.save(EXCEL_TEST_FILE_NAME)


print(len(CPP_FILES))
print(len(CAN_INTERFACE))

for i in range (0,len(CAN_INTERFACE)) :
    Line = CAN_INTERFACE[i]
    CAN_SIG_NAME       = Line.split(",")[0]
    INTERFACE_NAME     = Line.split(",")[1]
    ARXML_DATA_NAME    = Line.split(",")[2]
    INT_OUT_TYPE       = Line.split(",")[3]
    
    if (INT_OUT_TYPE == "In") :
        #get files function and line where the signal is readed
        #print (CAN_SIG_NAME)
        #Now parse all C and C++ file to find the function read
        CPP_FILE_FOUND = 0
        Counter_Nbr_File = 0
        while ((CPP_FILE_FOUND == 0) and (Counter_Nbr_File <len(CPP_FILES))) :
            CPP_F = CPP_FILES[Counter_Nbr_File]
            #read file
            Open_CPP_FILE = open (CPP_F , 'r')
            for LINE in  Open_CPP_FILE.readlines() :
                if ((INTERFACE_NAME in LINE ) and (ARXML_DATA_NAME in LINE ) and ('::Read' in LINE)):
                    #line found
                    CPP_FILE_FOUND = 1
                    SIG_INTERFACE.append(CAN_SIG_NAME + "," +INTERFACE_NAME+"::" +ARXML_DATA_NAME +"," + LINE +','+ CPP_F)
                    #print(CAN_SIG_NAME + "," +INTERFACE_NAME+"::" +ARXML_DATA_NAME +"," + LINE +','+ CPP_F)
                    break
            Counter_Nbr_File =Counter_Nbr_File + 1
            Open_CPP_FILE.close()
        if    (CPP_FILE_FOUND == 0):
            SIG_INTERFACE_NOT_FOUND.append(CAN_SIG_NAME+','+INTERFACE_NAME+"::" +ARXML_DATA_NAME)
            print ("Interface :"+ ARXML_DATA_NAME + " not prensent in the interface :" + INTERFACE_NAME + "Please check and create JIRA Ticket if NOT OK")
        
#Now create Test
#1 - GET SIGNAL INFORMATION
XML_DBC_FILE_TREE = etree.parse(XML_DBC_FILE)
for Node in XML_DBC_FILE_TREE.xpath("/Network/Node/Name"):
    print(Node.text)
#2 - create XML File

#DBC_TO_XML_FILE = convert(CAN_DBC_FILE, CAN_DBC_DIR+"fileout.xml")
#create_XSLX_FILE(EXCEL_TEST_FILE )

#2 - Create CAPL
#3 - Create TEST EXCEL
#4 - Create HTML file report


        
    
