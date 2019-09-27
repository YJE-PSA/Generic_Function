#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      U560764
#
# Created:     01/09/2019
# Copyright:   (c) U560764 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#CRC Calculation
Str1='100000F0F0BDE303E801FE0201000007'

VAL=0

for i in range(0,int(len(Str1)/2)) :
    #print(Str1[2*i:2*(i+1)])
    VAL = (VAL+int(Str1[2*i:2*(i+1)],16))
VAL_HEX=hex(VAL)
VAL_HEX=VAL_HEX[len(VAL_HEX)-2:len(VAL_HEX)]
CRC = str(hex(255-int(VAL_HEX,16)))
print( CRC)