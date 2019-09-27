#-------------------------------------------------------------------------------
# Name:        Analyze_map_file_functions
# Purpose:
#
# Author:      U560764
#
# Created:     09/06/2019
# Copyright:   (c) U560764 2019
# Licence:     PSA_Licence
#-------------------------------------------------------------------------------
def Generate_MAP_FILE_Information(MapFileRead):

    Image_Summary=[]
    Module_Summary=[]
    Global_Symbols=[]



    LineMapFile=MapFileRead.readline()

    while (LineMapFile != ''):
        LineMapFile=MapFileRead.readline()
        if ("  Section              Base      Size(hex)    Size(dec)  SecOffs" in LineMapFile):
            LineMapFile=MapFileRead.readline()
            while((LineMapFile != '') and (len(LineMapFile) > 8)):
                Image_Summary.append(LineMapFile)
                LineMapFile=MapFileRead.readline()
        if ("  Origin+Size    Section          Module"in LineMapFile):
            LineMapFile=MapFileRead.readline()
            while((LineMapFile != '') and (len(LineMapFile) > 8)):
                Module_Summary.append(LineMapFile)
                LineMapFile=MapFileRead.readline()

        if ("Global Symbols " in LineMapFile):
            LineMapFile=MapFileRead.readline()
            LineMapFile=MapFileRead.readline()
            while((LineMapFile != '') and (len(LineMapFile) > 8)):
                Global_Symbols.append(LineMapFile)
                LineMapFile=MapFileRead.readline()
    return Image_Summary, sorted(Module_Summary),Global_Symbols

