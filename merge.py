#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 11:27:10 2021

@author: mustafa
"""

import pandas as pd
import numpy as np
import glob
import os

def common_folders():
    s1 = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/S1/*")
    s2 = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/S2/*")
    infoPath = "/home/mustafa/Projects/1000/micro_v2/info1/info/"
    s1_folder = []
    s2_folder=[]
    for s1Csv in s1:
    #    print("s1Csv: ",s1Csv)
        s1_folder.append(os.path.basename(s1Csv))
        s11 = list(set(s1_folder))
        for s2Csv in s2:
    #        print("s2Csv:" ,s2Csv)
            s2_folder.append(os.path.basename(s2Csv))
            s21 = list(set(s2_folder))
            common_files = list(set(s11) & set(s21))
            for i in common_files:
                if(os.path.basename(s1Csv) == os.path.basename(s2Csv)):
                    if(not os.path.exists(infoPath+os.path.basename(s1Csv))):
    #                    print("true, creating dir")
                        os.mkdir(infoPath+os.path.basename(s1Csv))
                    t = glob.glob(s1Csv+"/*.csv")
                    t1 = glob.glob(s2Csv+"/*.csv")
                    list1 = os.listdir(s1Csv)
                    list2 = os.listdir(s2Csv)
                    c_files = set(list1) & set(list2)   
                    nc_files = set(list1) ^ set(list2)
                    csv1i = 0
                    for common in c_files:
                        csv1i = 0
                        for csv1 in t:
                            if(os.path.basename(csv1)==common):
                                csv1i  += 1
                                s1File  = pd.DataFrame()
                                s1File = pd.read_csv(csv1)
                                if(s1File.empty):
    #                                print("S1 is empty will continue to next csv")
                                    continue
                                else:
    #                                print("S1 is !empty will proceed")
                                    csv2i = 0
                                    for csv2 in t1:
                                        if(os.path.basename(csv2)==common):
                                            csv2i += 1
                                            if(os.path.basename(csv1) == os.path.basename(csv2)):
    #                                            print("s2: ",os.path.basename(csv1), " & ", os.path.basename(csv2))
                                                try:
                                                    s2File  = pd.DataFrame()
                                                    s2File = pd.read_csv(csv2)
                                                    if(s2File.empty):
                                                        continue
                                                    else:
                                                        merged = pd.concat([s1File,s2File])
                                                        merged.replace('None', np.nan, inplace=True)
                                                        merged = merged.mask(merged == 'NaN')
                                                        merged = (merged.sort_values(['Date']).groupby(['Date']).apply(lambda x: x.ffill().bfill()).drop_duplicates())
                                                        merged.replace(np.nan,'None', inplace=True)
                                                        merged.set_index('Date', inplace=True)
    #                                                    print("saving csv:", infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))
                                                        merged.to_csv(infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))        
                                                except:
                                                    s1File.set_index('Date', inplace=True)
                                                    s1File.to_csv(infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))
                    for notcommon in nc_files:
                        csv1i = 0
                        for csv1 in t:
                            if(os.path.basename(csv1)==notcommon):
                                csv1i  += 1
                                s1File  = pd.DataFrame()
                                s1File = pd.read_csv(csv1)
                                s1File.set_index('Date', inplace=True)
    #                            print("missing csv in s2:", infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))
                                s1File.to_csv(infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))
                        csv2i = 0
                        for csv2 in t1:
                            if(os.path.basename(csv2)==notcommon):
                                csv2i  += 1
                                try:
                                    s2File  = pd.DataFrame()
                                    s2File = pd.read_csv(csv2)
                                    if(s2File.empty):
                                        continue
                                    else:
                                        s2File.set_index('Date', inplace=True)
    #                                    print("missing csv in s1:", infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                                        s2File.to_csv(infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                                except:
                                    s2File.to_csv(infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                    break       
    print("common_folders",common_files)
    print(len(common_files))
    
def s1_folder():
    s1 = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/S1/*")
    info = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/info/*")
    infoPath = "/home/mustafa/Projects/1000/micro_v2/info1/info/"
    s1_folder = []
    info_folder=[]
    for s1Csv in s1:
    #    print("s1Csv: ",s1Csv)
        s1_folder.append(os.path.basename(s1Csv))
        s11 = list(set(s1_folder))
        for file in info:
            info_folder.append(os.path.basename(file))
            info1 = list(set(info_folder))
            nc = list(set(s11) ^ set(info1))
            for d in nc:
                for e in s11:
                    if d == e:
                        if(os.path.basename(s1Csv) ==d ):
                            if(not os.path.exists(infoPath+os.path.basename(s1Csv))):
                                os.mkdir(infoPath+os.path.basename(s1Csv))
                            t2 = glob.glob(s1Csv+"/*.csv")
                            csv1i = 0
                            for csv1 in t2:
                                csv1i  += 1
                                s1File  = pd.DataFrame()
                                s1File = pd.read_csv(csv1)
                                s1File.set_index('Date', inplace=True)
                                s1File.to_csv(infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))
                            break
    print("folders only in s1",nc)
    print(len(nc))
    
def s2_folder():
    s2 = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/S2/*")
    info = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/info/*")
    infoPath = "/home/mustafa/Projects/1000/micro_v2/info1/info/"
    s2_folder = []
    info_folder1=[]
    for s2Csv in s2:
    #    print("s1Csv: ",s1Csv)
        s2_folder.append(os.path.basename(s2Csv))
        s21 = list(set(s2_folder))
        for file in info:
            info_folder1.append(os.path.basename(file))
            info1 = list(set(info_folder1))
            nc1 = list(set(s21) ^ set(info1))
            for d in nc1:
                for e in s21:
                    if d == e:
                        if(os.path.basename(s2Csv) ==d ):
                            if(not os.path.exists(infoPath+os.path.basename(s2Csv))):
                                os.mkdir(infoPath+os.path.basename(s2Csv))
                            t3 = glob.glob(s2Csv+"/*.csv")
                            csv2i = 0
                            for csv2 in t3:
                                csv2i  += 1
                                try:
                                    s2File  = pd.DataFrame()
                                    s2File = pd.read_csv(csv2)
                                    if(s2File.empty):
                                        continue
                                    else:
                                        s2File.set_index('Date', inplace=True)
                                        s2File.to_csv(infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                                except:
                                    s2File.to_csv(infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                            break
    print("folders only in s2",nc1)
    print(len(nc1))
    
common_folders()
s1_folder()
s2_folder()