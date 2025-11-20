#!/usr/bin/env python3

import itertools
import glob
import sys

def Allele_Lister(input_MLST):
    """Makes a list of the possible allele combinations from a MLST file"""
    f = open(input_MLST, 'r')
    String1 = f.readline()
    f.close()
    Alleles = String1.split('\t')[3:]
    Matches = []
    for allele in Alleles:
        entry = Paranthese_Data(allele)
        alleles = entry.split(',')
        Matches.append(alleles)
    Info = list(itertools.product(*Matches))
    Out = []
    for entry in Info:
        List1 = list(entry)
        Out.append(List1)
    return Out

def Repeat_Remover(any_list):
    """Removes repeats for any list"""
    new_list = []
    for items in any_list:
        if (items in new_list) == False:
            new_list.append(items)
    return new_list

def Allele_Lister_Line(input_MLST_line):
    """Makes a list of the possible allele combinations from a MLST line"""
    String1 = input_MLST_line
    Alleles = String1.split('\t')[3:]
    Matches = []
    for allele in Alleles:
        entry = Paranthese_Data(allele)
        alleles = entry.split(',')
        alleles = Repeat_Remover(alleles)
        Matches.append(alleles)
    Info = list(itertools.product(*Matches))
    Out = []
    for entry in Info:
        List1 = list(entry)
        Out.append(List1)
    return Out

def Paranthese_Data(input_string):
    """Returns the data enclosed by parantheses "()" in a string"""
    Out = ''
    Add = 0
    for entry in input_string:
        if Add == 1 and entry != ')':
            Out = Out + entry
        elif entry == '(':
            Add = 1
        elif entry == ')':
            Add = 0
    return Out

def ST_Lister(input_MLST_Scheme):
    Out = [[], []]
    f = open(input_MLST_Scheme)
    String1 = f.readline()
    for line in f:
        List1 = line.split()
        Out[0].append(List1[0])
        Out[1].append(List1[1:8])
    f.close()
    return Out

def ST_Matcher(MLST_Scheme_List, MLST_file):
    Match_List = Allele_Lister(MLST_file)
    MLST_ST = MLST_Scheme_List[0]
    MLST_Profiles = MLST_Scheme_List[1]
    STs = []
    for entry in Match_List:
        ST = 'NM'
        if (entry in MLST_Profiles):
            Pos = MLST_Profiles.index(entry)
            ST = MLST_ST[Pos]
        STs.append(ST)
    STs.sort()
    return STs

def ST_Matcher_Line(MLST_Scheme_List, MLST_Line):
    Match_List = Allele_Lister_Line(MLST_Line)
    MLST_ST = MLST_Scheme_List[0]
    MLST_Profiles = MLST_Scheme_List[1]
    STs = []
    for entry in Match_List:
        ST = 'NM'
        if (entry in MLST_Profiles):
            Pos = MLST_Profiles.index(entry)
            ST = MLST_ST[Pos]
        STs.append(ST)
    Out = Number_Sorter(STs)
    return Out

def Number_Sorter(input_list):
    New = []
    Novel = []
    for entry in input_list:
        if entry == 'NM':
            Novel.append(entry)
        else:
            New.append(int(entry))
    New.sort()
    Out = []
    for entry in New:
        Out.append(str(entry))
    for entry in Novel:
        Out.append(entry)
    return Out

def MLST_Combined_Output(MLST_Combined_file, MLST_Scheme_File):
    """Reads in a cat MLST compbined file and makes an output of the names and STs"""
    f = open(MLST_Combined_file, 'r')
    Out = open(MLST_Combined_file + '.Combination_STs.txt', 'w')
    Out.write('ID\tMLST\n')
    MLST_List = ST_Lister(MLST_Scheme_File)
    for line in f:
        Name = line.split('\t')[0]
        ST = ST_Matcher_Line(MLST_List, line)
        ST = ','.join(ST)
        Out.write(Name + '\t' + ST + '\n')
    f.close()
    Out.close()

MLST_Combined_Output(sys.argv[1], sys.argv[2])
