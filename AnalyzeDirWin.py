#######################################################
# PSA
# date: 18/01/2019
# username:
# name: YJE
# description: return the message of a given signal
#######################################################
#!/usr/bin/env python

######################################################
#import section
import sys
import os
import re
import operator
from xml.sax.saxutils import quoteattr as xml_quoteattr
######################################################


#Function section
######################################################
def gen_flist(dir_path, dir_name):
    with os.scandir(dir_path) as listOfEntries:  
        for entry in listOfEntries:
            if entry.is_dir():
                gen_flist(entry.path, dir_name)
            elif entry.name.lower().endswith(('.c', '.cpp', '.h')):
                shutil.copy2(entry.path, output_directory + entry.name)
                
                current_path, current_name = os.path.split(os.path.abspath(entry))
                store_data(current_name, current_path);
######################################################

######################################################
def scan_dir(dir):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            fileName = path.split('\\')[len(path.split('\\'))-1]
            
            print (path.replace(fileName, ""))
        else:
            scan_dir(path)
######################################################
            
######################################################

def dirToXML(self,directory):
        curdir = os.getcwd()
        os.chdir(directory)
        xmlOutput=""

        tree = os.walk(directory)
        for root, dirs, files in tree:
            pathName = string.split(directory, os.sep)
            xmlOutput+="<dir><name><![CDATA["+pathName.pop()+"]]></name>"
            if (len(files)>0) and (files.name.lower().endswith(('.c', '.cpp', '.h','.hpp','.bat'))):
                xmlOutput+=self.fileToXML(files)
            for subdir in dirs:
                xmlOutput+=self.dirToXML(os.path.join(root,subdir))
            xmlOutput+="</dir>"

        os.chdir(curdir)
        return xmlOutput  
######################################################
    
######################################################    
def DirAsLessXML(path):
    xmlOutput = '<dir name=%s>\n' % xml_quoteattr(os.path.basename(path))
    for item in os.listdir(path):
        itempath = os.path.join(path, item)
        if os.path.isdir(itempath):
            xmlOutput += '\n'.join('  ' + line for line in 
                DirAsLessXML(os.path.join(path, item)).split('\n'))
        elif os.path.isfile(itempath):
            xmlOutput += '  <file name=%s />\n' % xml_quoteattr(item)
    xmlOutput += '</dir>\n'
    return xmlOutput
######################################################


scan_dir("C:/ADAS/Draft_Software/ProjPSA/Customer")