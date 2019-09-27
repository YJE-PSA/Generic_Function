#-------------------------------------------------------------------------------
# Name:        Generate_ULP_FILE
# Purpose:
#
# Author:      U560764
#
# Created:     30/08/2019
# Copyright:   (c) U560764 2019
# Licence:     PSA
#-------------------------------------------------------------------------------
import sys, string, os#, arcgisscripting
from random import *
import argparse



def Fill_Gaps_Line(Exe_file,File_In_,File_Out_,Add_Beg,Add_Fin,Gaps_Byte):
    return Exe_file + ' '+ File_In_+' -intel -fill' +' ' + Gaps_Byte + ' ' + Add_Beg + ' ' + Add_Fin + ' -o ' + File_Out_ +' -intel'
def Check_EXE_exist():
    if (os.path.isfile(SREC_CAT_EXE) and os.path.isfile(SREC_CMP_EXE) and os.path.join(SREC_INFO_EXE))  :
        return True
    else :
        return False

def Check_Add(Add):
    list_aut = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','a','b','c','d','e','f']
    if((Add[0:2] =='0x') or (Add[0,2] =='0X')):
        if len(Add) == len('0x80000000') :
            #len is OK
            for i in range(2,len(Add)):
                if (Add[i:i+1] not in list_aut ) :
                    return 1
            return 0
        else :
            return 1
    else :
        return 1

def Delete_File(File_To_Delete):
    os.remove(File_To_Delete)
def Concat_Hex_Line(EXE_FILE, File_IN_1,File_IN_2,File_Out):
    return EXE_FILE +' ' +File_IN_1 + ' -intel' + ' ' +File_IN_2 + ' -intel' + ' -o '+File_Out + ' -intel'
def Concat_Hex_Files(File_IN_1,File_IN_2,File_Out) :
    #on this function we call exe
    #check exe exist
    DIR_EXE_FILE = 'C:/ADAS/ec400/Development/Scripts_Integration/ULP_GENERATION'
    srec_cat='srec_cat.exe'
    srec_cmp='srec_cmp.exe'
    srec_info='srec_info.exe'
    SREC_CAT_EXE = os.path.join(DIR_EXE_FILE,srec_cat)
    SREC_CMP_EXE = os.path.join(DIR_EXE_FILE,srec_cmp)
    SREC_INFO_EXE = os.path.join(DIR_EXE_FILE,srec_info)
    if (Check_EXE_exist() is True)  :
        #EXE files exist so concat files
        #check HEX files exists
        if (os.path.isfile(File_IN_1) and os.path.isfile(File_IN_2)):
            #check if file File_Out exist delete it
            if (os.path.isfile(File_Out)):
                Delete_File(File_Out)
            if (os.path.isfile(File_Out)):
                File_Out = os.path.join(os.path.dirname(File_Out),'FileHex'+str(random(1,255)))
            #now all is prepared

            Concat_line = Concat_Hex_Line(SREC_CAT_EXE,File_IN_1,File_IN_2,File_Out)
            print('Concat line',Concat_line)
            os.system(Concat_line)
            if(os.path.isfile(File_Out)):
                return 0
            else :
                return 1
        else :
            return 2 #no files to concat
    else:
        print('3')
        return 3 # no exe files


def Fill_Gaps_In_File(File_In,File_Out,Add_Begin,Add_Fin,Gaps_Byte):
    if(os.path.isfile(File_In)):
        #file exist
        if((Check_Add(Add_Begin) ==0 ) and (Check_Add(Add_Fin)==0)):
            if((Gaps_Byte[0:2]=='0x' or Gaps_Byte[0:2]=='0X') and (Gaps_Byte[2:4]=='FF' or Gaps_Byte[2:4]=='ff' or Gaps_Byte[2:4]=='00')  ) :
                Line_Fill_Gabs = Fill_Gaps_Line(SREC_CAT_EXE,File_In,File_Out,Add_Begin,Add_Fin,Gaps_Byte)

                if (Check_EXE_exist() is True):
                    print(Line_Fill_Gabs)
                    os.system(Line_Fill_Gabs)
                else :
                    return 3
            else:
                return 4 #Gaps byte is wrong
        else :
            return 5 #Address Begin and End are Wrong
    else :
        return 2
def Convert_Hex_To_S19_Line(EXE_File, File1_In,File2_Out):
    return EXE_File +' ' + File1_In+ ' -intel ' + '-o ' + File2_Out
def Convert_Hex_To_S19(File_In_,File_Out_):
    #check file 1 exist
    if (os.path.isfile(File_In_)) :
        line_Convert = Convert_Hex_To_S19_Line(SREC_CAT_EXE,File_In_,File_Out_)
        print(line_Convert)
        os.system(line_Convert)
def Add_CRC_File_Add_Line(EXE_File,File1_In,File2_Out,Addres):
    return EXE_File + ' '+ File1_In + ' -crop 0 ' + Addres + ' -crc32-b-e ' + Addres + ' -o '+ File2_Out
def Add_CRC_File_Add(File_In_,File_Out_,Add_CRC):
    #check if file1 exist
    if (os.path.isfile(File_In_)) :
        Line_Add_CRC = Add_CRC_File_Add_Line(SREC_CAT_EXE,File_In_,File_Out_,Add_CRC)
        print(Line_Add_CRC)
        os.system(Line_Add_CRC)
def CALC_CRC(Str1):
    VAL=0

    for i in range(0,int(len(Str1)/2)) :
        #print(Str1[2*i:2*(i+1)])
        VAL = (VAL+int(Str1[2*i:2*(i+1)],16))
    VAL_HEX=hex(VAL)
    VAL_HEX=VAL_HEX[len(VAL_HEX)-2:len(VAL_HEX)]
    CRC = str(hex(255-int(VAL_HEX,16)))
    return CRC[2:4]
def Write_ZI_ZA_IN_ULP(ULP_REF,CLEF_APPLI,Supplier_Code,System_Code,Application_Code,Software_Version_Code,Software_Edition_Code):
    #ZI_ZA is organized like this
    #'S1100000F0F0' +CLEF_APPLI + Supplier_Code + System_Code +Application_Code + Software_Version_Code + Software_Edition_Code + ULP_REF[2:len(ULP_REF)-2] + CRC of line
    CRC=CALC_CRC('100000F0F0' +CLEF_APPLI + Supplier_Code + System_Code +Application_Code + Software_Version_Code + Software_Edition_Code + ULP_REF[2:len(ULP_REF)-2])
    return 'S1100000F0F0' +CLEF_APPLI + Supplier_Code + System_Code +Application_Code + Software_Version_Code + Software_Edition_Code + ULP_REF[2:len(ULP_REF)-2] +CRC
def Create_ULP_File(Hex_File_In_,ULP_File_Out_,ULP_REF,CLEF_APPLI,Supplier_Code,System_Code,Application_Code,Software_Version_Code,Software_Edition_Code) :
    if(os.path.isfile(Hex_File_In_)) :
        #open file in read Hex_File_In_
        read_In_File = open(Hex_File_In_,'r')
        #open File in write Mode ULP_File_Out_
        Write_Out_File = open(ULP_File_Out_,'w')
        #Create Header One
        Write_Out_File.write('S00C0000960000000101820000D9'+'\n')
        Line_ZI_ZA =Write_ZI_ZA_IN_ULP(ULP_REF,CLEF_APPLI,Supplier_Code,System_Code,Application_Code,Software_Version_Code,Software_Edition_Code)
        Write_Out_File.write(Line_ZI_ZA+'\n')
        for lines in read_In_File.readlines() :
            if(lines[0:2] =='S3'):
                Write_Out_File.write(lines)
        Write_Out_File.write('S70500000000FA')

#STR_Entry_App_File_In,STR_Entry_CAL_File_In,STR_Entry_Path_Out.get(),STR_Entry_File_Out.get(),STR_Entry_ULP_REF.get(),STR_Entry_CLEF_APPLI.get(),STR_Entry_Supplier_Code.get(),STR_Entry_System_Code.get(),STR_Entry_Application_Code.get(),STR_Entry_Software_Version_Code.get(),STR_Entry_Software_Edition_Code.get())=
        print('OK')
def Generate_ULP(App_file1,Cal_File1,PATH_OUT_Dir,ULP_File_Out_Name, ULP_REF, CLEF_APPLI, Supplier_Code, System_Code, Application_Code, Software_Version_Code, Software_Edition_Code):
    HEX_OXI_FILE = os.path.join(PATH_OUT_Dir,'OXI_File_Tobedeleted.hex')
    S19_OXI_FILE = os.path.join(PATH_OUT_Dir,'OXI_File_Tobedeleted.s19')
    S19_CRC_OXI_FILE = os.path.join(PATH_OUT_Dir,'OXI_CRC_File_Tobedeleted.s19')
    ULP_FILE_Output=os.path.join(PATH_OUT_Dir,ULP_File_Out_Name)
    Concat_Hex_Files(App_file1,Cal_File1,HEX_OXI_FILE)
    Fill_Gaps_In_File(HEX_OXI_FILE,HEX_OXI_FILE,'0x80068000','0x80200000','0xFF')
    Fill_Gaps_In_File(HEX_OXI_FILE,HEX_OXI_FILE,'0x80300000','0x804C7FFC','0xFF')
    Convert_Hex_To_S19(HEX_OXI_FILE,S19_OXI_FILE)
    Add_CRC_File_Add(S19_OXI_FILE,S19_CRC_OXI_FILE,'0x804C7FFC')
    Create_ULP_File(S19_CRC_OXI_FILE,ULP_FILE_Output, ULP_REF, CLEF_APPLI, Supplier_Code, System_Code, Application_Code, Software_Version_Code, Software_Edition_Code)
    if (os.path.isfile(ULP_FILE_Output)) :
        os.remove(HEX_OXI_FILE    )
        os.remove(S19_OXI_FILE    )
        os.remove(S19_CRC_OXI_FILE)
        print('OK')
        return True
    else :
        #dont delete to see whats Happen
        return 0
    print('OK')

DIR_EXE_FILE = 'C:/ADAS/ec400/Development/Scripts_Integration/ULP_GENERATION'
srec_cat='srec_cat.exe'
srec_cmp='srec_cmp.exe'
srec_info='srec_info.exe'
SREC_CAT_EXE = os.path.join(DIR_EXE_FILE,srec_cat)
SREC_CMP_EXE = os.path.join(DIR_EXE_FILE,srec_cmp)
SREC_INFO_EXE = os.path.join(DIR_EXE_FILE,srec_info)

#-----------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------
#parse argument
parser = argparse.ArgumentParser()
parser.add_argument('App_file1'             , type=str, help="Application Hex file   ")
parser.add_argument('Cal_File1'             , type=str, help="Calibration Hex file   ")
parser.add_argument('PATH_OUT_Dir'          , type=str, help="Path of output ULP file")
parser.add_argument('ULP_File_Out_Name'     , type=str, help="Name of output ULP file")
parser.add_argument('ULP_REF'               , type=str, help="ULP REF                ")
parser.add_argument('CLEF_APPLI'            , type=str, help="CLEF APPLI             ")
parser.add_argument('Supplier_Code'         , type=str, help="Supplier Code          ")
parser.add_argument('System_Code'           , type=str, help="System Code            ")
parser.add_argument('Application_Code'      , type=str, help="Application Code       ")
parser.add_argument('Software_Version_Code' , type=str, help="Software Version Code  ")
parser.add_argument('Software_Edition_Code' , type=str, help="Software Edition Code  ")
parser.add_argument("-v", "--verbosity", action="count", default=0)
args = parser.parse_args()
App_file1            = args.App_file1
Cal_File1            = args.Cal_File1
PATH_OUT_Dir         = args.PATH_OUT_Dir
ULP_File_Out_Name    = args.ULP_File_Out_Name
ULP_REF              = args.ULP_REF
CLEF_APPLI           = args.CLEF_APPLI
Supplier_Code        = args.Supplier_Code
System_Code          = args.System_Code
Application_Code     = args.Application_Code
Software_Version_Code= args.Software_Version_Code
Software_Edition_Code= args.Software_Edition_Code
##App_file1            = 'C:/WORK/Script/HEX_MANIPULATION/Test/PSA_ADAS.hex'
##Cal_File1            = 'C:/WORK/Script/HEX_MANIPULATION/Test/Cal.hex'
##PATH_OUT_Dir         = 'C:/WORK/Script/HEX_MANIPULATION/Test'
##ULP_File_Out_Name    = 'Calib_APPL_File.ULP'
##ULP_REF              = '9600001280'
##CLEF_APPLI           = 'BDE3'
##Supplier_Code        = '03'
##System_Code          = 'E8'
##Application_Code     = '01'
##Software_Version_Code= 'FC'
##Software_Edition_Code= '0301'
print(App_file1            )
print(Cal_File1            )
print(PATH_OUT_Dir         )
print(ULP_File_Out_Name    )
print(ULP_REF              )
print(CLEF_APPLI           )
print(Supplier_Code        )
print(System_Code          )
print(Application_Code     )
print(Software_Version_Code)
print(Software_Edition_Code)
Generate_ULP(App_file1,Cal_File1,PATH_OUT_Dir,ULP_File_Out_Name, ULP_REF, CLEF_APPLI, Supplier_Code, System_Code, Application_Code, Software_Version_Code, Software_Edition_Code)
##file1='C:/WORK/Script/HEX_MANIPULATION/Test/Cal.hex'
##file2='C:/WORK/Script/HEX_MANIPULATION/Test/PSA_ADAS.hex'
##file1_2='C:/WORK/Script/HEX_MANIPULATION/Test/Cal_PSA_ADAS.hex'
##file1_2_S19='C:/WORK/Script/HEX_MANIPULATION/Test/Cal_PSA_ADAS.s19'
##file1_2_S19_CRC='C:/WORK/Script/HEX_MANIPULATION/Test/Cal_PSA_ADAS_CRC.s19'
##
##
##file5='C:/WORK/Script/HEX_MANIPULATION/Test/ULP.ULP'
##
###to create an ULP file
###Concat App Hex to Cal Hex
##Concat_Hex_Files(file1,file2,file1_2)
##
###Fill Gaps with 0xFF from add 0x80068000 to add 0x80200000
##Fill_Gaps_In_File(file1_2,file1_2,'0x80068000','0x80200000','0xFF')
##
##
###Fill Gaps with 0xFF from add 0x80300000 to add 0x804C7FFC
##Fill_Gaps_In_File(file1_2,file1_2,'0x80300000','0x804C7FFC','0xFF')
##
###convert to S19 extension file
##Convert_Hex_To_S19(file1_2,file1_2_S19)
###add SRC at the End of the file 0x804C7FFC
##Add_CRC_File_Add(file1_2_S19,file1_2_S19_CRC,'0x804C7FFC')
###create ULP file file_In,File_Out,            ULP_REF,    CLEF_APPLI,Supplier_Code,System_Code,Application_Code,Software_Version_Code,Software_Edition_Code
##Create_ULP_File(file1_2_S19_CRC,file5,       '9600000780','BDE3',   '03',         'E8',       '01',            'FE',                 '0201')
##
##os.remove(file1_2)
##os.remove(file1_2_S19)
##os.remove(file1_2_S19_CRC)