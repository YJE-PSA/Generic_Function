#-------------------------------------------------------------------------------
# Name:        Generate_CppDeps.py
# Purpose:     Generate dependency for C++ project
#
# Author:      U560764
#
# Created:     29/05/2019
# Copyright:   (c) U560764 2019
# Licence:     PSA Licence
#-------------------------------------------------------------------------------


#----------------------------------------------------------------------------
#------------------------------ IMPORT---------------------------------------
#----------------------------------------------------------------------------
import os
import sys
import re
import operator
import argparse
import logging
from logging.handlers import RotatingFileHandler

import networkx as nx
import matplotlib.pyplot as plt
#----------------------------------------------------------------------------
#------------------------------ Function ------------------------------------
#----------------------------------------------------------------------------
def Get_List_Of_Files(dir,Filter1,Filter2,Filter3):
    global Tableau_PATH
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            fileName = path.split('\\')[len(path.split('\\'))-1]
            if (fileName.endswith(Filter1) or fileName.endswith(Filter2) or fileName.endswith(Filter3)) :
                Tableau_PATH.append(path)
                #print (path)
        else:
            Get_List_Of_Files(path,Filter1,Filter2,Filter3)

#-----------------------------------------------------------------------------------------------------------------------------------------
# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
# création d'un handler qui va rediriger une écriture du log vers
# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
file_handler = RotatingFileHandler('Generate_CppDeps.log', 'a', 1000000, 1)
# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
# créé précédement et on ajoute ce handler au logger
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
#-----------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------
#parse argument
parser = argparse.ArgumentParser()
parser.add_argument("Path", type=str, help="the Project Path")
parser.add_argument("PNG_NAME", type=str, help="the PNG image name")
parser.add_argument("-v", "--verbosity", action="count", default=0)
args = parser.parse_args()
PATH_PROJ=args.Path
PNG_NAME_FILE =args.PNG_NAME
print(args.Path)
print(args.PNG_NAME)

#-----------------------------------------------------------------------------------------------------------------------------------------
#parse argument
if args.verbosity :
    logger.disable=False
    print("generating the depends graph of the project located in '{}'".format(args.x))
if args.verbosity >= 1:
    logger.disable=True
Tableau_PATH = []
Tableau_NAME = []
Get_List_Of_Files(PATH_PROJ,".h",".c",".cpp")
logger.info("begin analyze path")
for pth in Tableau_PATH :
    Tableau_NAME.append(os.path.basename(pth))

Tableau_NAME = set(Tableau_NAME)
print(len(Tableau_NAME))
print(len(Tableau_PATH))
#get list of duplacated files
#begin constract diag
#for each file print
Len_Tableau_PATH=len(Tableau_PATH)
Len_Tableau_NAME=len(Tableau_NAME)
if (Len_Tableau_PATH < Len_Tableau_NAME) :
    logger.warrning("Duplicated file found")
    logger.warrning("Duplicated file Will not be considered")
##    i=0
##    j=0
##    while (i<Len_Tableau_NAME) :
##        if Tableau_PATH[]

G = nx.Graph()

G.add_edges_from([(1, 2), (1, 3)])
G.add_node(1)
G.add_edge(1, 2)
G.add_node("spam")        # adds node "spam"
G.add_nodes_from("spam")  # adds 4 nodes: 's', 'p', 'a', 'm'
G.add_edge(3, 'm')

G = nx.petersen_graph()
plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold')
plt.subplot(122)
nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
plt.show()