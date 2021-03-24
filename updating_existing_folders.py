#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 15:55:54 2021

@author: mustafa
"""

import pandas as pd
import numpy as np
import glob
import os

def update_common_folders():
    s1 = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/S1/*")
    s2 = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/S2/*")
    info = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/info/*")
    infoPath = "/home/mustafa/Projects/1000/micro_v2/info1/info/"
    
    s1_folder = []
    s2_folder=[]
    info_folder=[]
    for s1Csv in s1:
    #    print("s1Csv: ",s1Csv)
        s1_folder.append(os.path.basename(s1Csv))
        s11 = list(set(s1_folder))
        for s2Csv in s2:
    #        print("s2Csv:" ,s2Csv)
            s2_folder.append(os.path.basename(s2Csv))
            s21 = list(set(s2_folder))
            for infoCsv in info:
                info_folder.append(os.path.basename(infoCsv))
                s31 = list(set(info_folder))
                common1 = list(set(s11) & set(s21))
                common2 = list(set(common1) & set(s31))
                common_file = list(set(common1) & set(common2))    
                s1_common = list(set(s11) ^  set(s31))
                s2_common = list(set(s21) ^ set(s31))
                nc_common = list(set(s1_common + s2_common))
                for i in common_file:
                    if((os.path.basename(s1Csv) ==i) and (os.path.basename(s2Csv) ==i) and (os.path.basename(infoCsv) ==i)):
#                        print(True)
                        t = glob.glob(s1Csv+"/*.csv")
                        t1 = glob.glob(s2Csv+"/*.csv")
                        t2 = glob.glob(infoCsv+"/*.csv")
                        list1 = os.listdir(s1Csv)
                        s1_files = len(list1)
                        list2 = os.listdir(s2Csv)
                        s2_files = len(list2)
                        list3 = os.listdir(infoCsv)
                        info_files = len(list3)
                        c_files = list(set(list1) & set(list2))
                        c_files1 = list(set(c_files) & set(list3))
                        nc_files = list(set(list1) ^ set(list2))
                        nc_files1 = list(set(list1) ^ set(list3))
                        nc_files2 = list(set(list2) ^ set(list3))
                        for common in c_files1:
                            csv1i = 0
                            for csv1 in t:
                                if(os.path.basename(csv1)==common):
#                                    print("inif s1 common",os.path.basename(csv1),common)
                                    csv1i  += 1
                                    try:
                                        s1File  = pd.DataFrame()
#                                        print("csv1",csv1)
                                        s1File = pd.read_csv(csv1)
                                        if(s1File.empty):
 #                                           print("S1 is empty will continue to next csv")
                                            continue
                                        else:
                                            s1_date = s1File.Date.tolist()
#                                            print("S1 is !empty will proceed")
#                                            print("length s1", len(s1_date))
                                    except:
                                        s1_date = []
#                                        print("no data in s1")
#                                        print("length s1", len(s1_date))
                                    csv2i = 0
                                    for csv2 in t1:
                                        if(os.path.basename(csv2)==common):
#                                            print("inif s2 common",os.path.basename(csv2),common)
                                            csv2i  += 1
                                            try:
                                                s2File  = pd.DataFrame()
#                                                print("csv2",csv2)
                                                s2File = pd.read_csv(csv2)
                                                if(s2File.empty):
#                                                    print("S2 is empty will continue to next csv")
                                                    continue
                                                else:
                                                    s2_date = s2File.Date.tolist()
#                                                    print("S2 is !empty will proceed")
#                                                    print("length s2", len(s2_date))
                                            except:
                                                s2_date = []
#                                                print("no data in s2")
#                                                print("length s2", len(s2_date))
                                            csv3i = 0
                                            for csv3 in t2:
                                                if(os.path.basename(csv3)==common):
#                                                    print("inif info common",os.path.basename(csv3),common)
                                                    csv3i  += 1 
                                                    try:
                                                        infioFile  = pd.DataFrame()
                                                        infioFile = pd.read_csv(csv3)
                                                        if(infioFile.empty):
#                                                            print("info is empty will continue to next csv")
                                                            continue
                                                        else:
                                                            info_date = infioFile.Date.tolist()
#                                                            print("info is !empty will proceed")
#                                                            print("length info", len(info_date))
                                                    except:
                                                        info_date = []
#                                                        print("no data in info")
#                                                        print("length info", len(info_date))
                                                        
                                                    if(not s2File.empty):    
                                                        s1_s2 = list(set(s1_date+s2_date))
#                                                        print(len(s1_s2))
                                                    else:
                                                        s1_s2 = list(set(s1_date))
#                                                        print(len(s1_s2))
                                                    if(len(s1_s2) != len(info_date)):
                                                        print("noteq!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                                        merged = pd.concat([s1File,s2File])
                                                        merged.replace('None', np.nan, inplace=True)
                                                        merged = merged.mask(merged == 'NaN')
                                                        merged = (merged.sort_values(['Date']).groupby(['Date']).apply(lambda x: x.ffill().bfill()).drop_duplicates())
                                                        merged.replace(np.nan,'None', inplace=True)
                                                        merged.set_index('Date', inplace=True)
                                                        print("saving csv:", infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))
                                                        merged.to_csv(infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))
                                                        print("merged",len(merged))
                        for s1common in nc_files1:
#                            print("inside s1")
                            csv1i = 0
                            for csv1 in t:
                                if(os.path.basename(csv1)==s1common):
#                                    print("inif s1 common",os.path.basename(csv1),s1common)
                                    csv1i  += 1
                                    try:
                                        s1File  = pd.DataFrame()
#                                        print("csv1",csv1)
                                        s1File = pd.read_csv(csv1)
                                        if(s1File.empty):
#                                            print("S1 is empty will continue to next csv")
                                            continue
                                        else:
                                            s1File.set_index('Date', inplace=True)
#                                            print("missing csv in info:", infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))
                                            s1File.to_csv(infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))
                                    except:
                                        s1File.set_index('Date', inplace=True)
#                                        print("missing csv in info:", infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))
                                        s1File.to_csv(infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1)) 
                        for s2common in nc_files2:
#                            print("inside s2")
                            csv2i = 0
                            for csv2 in t1:
                                if(os.path.basename(csv2)==s2common):
#                                    print("inif s2 common",os.path.basename(csv2),s2common)
                                    csv2i  += 1
                                    try:
                                        s2File  = pd.DataFrame()
#                                        print("csv2",csv2)
                                        s2File = pd.read_csv(csv2)
                                        if(s2File.empty):
#                                            print("S2 is empty will continue to next csv")
                                            continue
                                        else:
                                            s2File.set_index('Date', inplace=True)
                                            print("missing csv in info:", infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                                            s2File.to_csv(infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                                    except:
                                        s2File.set_index('Date', inplace=True)
                                        print("missing csv in info:", infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                                        s2File.to_csv(infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2)) 
                                    
                        break
                    
                    
                    
def update_common_s1_folders():
    s1 = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/S1/*")
    s2 = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/S2/*")
    info = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/info/*")
    infoPath = "/home/mustafa/Projects/1000/micro_v2/info1/info/"
    
    s1_folder = []
    s2_folder=[]
    info_folder=[]
    for s1Csv in s1:
    #    print("s1Csv: ",s1Csv)
        s1_folder.append(os.path.basename(s1Csv))
        s11 = list(set(s1_folder))
        for s2Csv in s2:
    #        print("s2Csv:" ,s2Csv)
            s2_folder.append(os.path.basename(s2Csv))
            s21 = list(set(s2_folder))
            for infoCsv in info:
                info_folder.append(os.path.basename(infoCsv))
                s31 = list(set(info_folder))
                common1 = list(set(s11) & set(s21))
                common2 = list(set(common1) & set(s31))
                common_file = list(set(common1) & set(common2))    
                s1_common = list(set(s11) ^  set(s31))
                s2_common = list(set(s21) ^ set(s31))
                nc_common = list(set(s1_common + s2_common))
                for i in common_file:
                    if((os.path.basename(s1Csv) ==i) and (os.path.basename(s2Csv) ==i) and (os.path.basename(infoCsv) ==i)):
#                        print(True)
                        t = glob.glob(s1Csv+"/*.csv")
                        t1 = glob.glob(s2Csv+"/*.csv")
                        t2 = glob.glob(infoCsv+"/*.csv")
                        list1 = os.listdir(s1Csv)
                        s1_files = len(list1)
                        list2 = os.listdir(s2Csv)
                        s2_files = len(list2)
                        list3 = os.listdir(infoCsv)
                        info_files = len(list3)
                        c_files = list(set(list1) & set(list2))
                        c_files1 = list(set(c_files) & set(list3))
                        nc_files = list(set(list1) ^ set(list2))
                        nc_files1 = list(set(list1) & set(list3) ^ set(list2))
                        for s1common in nc_files1:
                            csv1i = 0
                            for csv1 in t:
                                if(os.path.basename(csv1)==s1common):
#                                    print("inif s1 common",os.path.basename(csv1),s1common)
                                    csv1i  += 1
                                    try:
                                        s1File  = pd.DataFrame()
#                                        print("csv1",csv1)
                                        s1File = pd.read_csv(csv1)
                                        if(s1File.empty):
#                                            print("S1 is empty will continue to next csv")
                                            continue
                                        else:
                                            s1_date = s1File.Date.tolist()
#                                            print("S1 is !empty will proceed")
#                                            print("length s1", len(s1_date))
                                    except:
                                        s1_date = []
#                                        print("no data in s1")
#                                        print("length s1", len(s1_date))
                                    csv3i = 0
                                    for csv3 in t2:
                                        if(os.path.basename(csv3)==s1common):
#                                            print("inif info s1common",os.path.basename(csv3),s1common)
                                            csv3i  += 1 
                                            try:
                                                infioFile  = pd.DataFrame()
                                                infioFile = pd.read_csv(csv3)
                                                if(infioFile.empty):
#                                                    print("info is empty will continue to next csv")
                                                    continue
                                                else:
                                                    info_date = infioFile.Date.tolist()
#                                                    print("info is !empty will proceed")
#                                                    print("length info", len(info_date))
                                            except:
                                                info_date = []
#                                                print("no data in info")
#                                                print("length info", len(info_date))
                                                   
                                            s1_s2 = list(set(s1_date))
#                                            print(len(s1_s2))
                                            
                                            if(len(s1_s2) != len(info_date)):
                                                print("noteq!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                                s1File.set_index('Date', inplace=True)
                                                print("missing csv in info:", infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))
                                                s1File.to_csv(infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))
                        break                   


def update_common_s2_folders():

    s1 = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/S1/*")
    s2 = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/S2/*")
    info = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/info/*")
    infoPath = "/home/mustafa/Projects/1000/micro_v2/info1/info/"
    
    s1_folder = []
    s2_folder=[]
    info_folder=[]
    for s1Csv in s1:
    #    print("s1Csv: ",s1Csv)
        s1_folder.append(os.path.basename(s1Csv))
        s11 = list(set(s1_folder))
        for s2Csv in s2:
    #        print("s2Csv:" ,s2Csv)
            s2_folder.append(os.path.basename(s2Csv))
            s21 = list(set(s2_folder))
            for infoCsv in info:
                info_folder.append(os.path.basename(infoCsv))
                s31 = list(set(info_folder))
                common1 = list(set(s11) & set(s21))
                common2 = list(set(common1) & set(s31))
                common_file = list(set(common1) & set(common2))    
                s1_common = list(set(s11) ^  set(s31))
                s2_common = list(set(s21) ^ set(s31))
                nc_common = list(set(s1_common + s2_common))
                for i in common_file:
                    if((os.path.basename(s1Csv) ==i) and (os.path.basename(s2Csv) ==i) and (os.path.basename(infoCsv) ==i)):
#                        print(True)
                        t = glob.glob(s1Csv+"/*.csv")
                        t1 = glob.glob(s2Csv+"/*.csv")
                        t2 = glob.glob(infoCsv+"/*.csv")
                        list1 = os.listdir(s1Csv)
                        s1_files = len(list1)
                        list2 = os.listdir(s2Csv)
                        s2_files = len(list2)
                        list3 = os.listdir(infoCsv)
                        info_files = len(list3)
                        c_files = list(set(list1) & set(list2))
                        c_files1 = list(set(c_files) & set(list3))
                        nc_files = list(set(list1) ^ set(list2))
                        nc_files1 = list(set(list1) & set(list3))
                        nc_files2 = list(set(list2) & set(list3) ^ set(list1))
                        for s2common in nc_files2:
                            csv2i = 0
                            for csv2 in t1:
                                if(os.path.basename(csv2)==s2common):
#                                    print("inif s2 common",os.path.basename(csv2),s2common)
                                    csv2i  += 1
                                    try:
                                        s2File  = pd.DataFrame()
#                                        print("csv2",csv2)
                                        s2File = pd.read_csv(csv2)
                                        if(s2File.empty):
#                                            print("S2 is empty will continue to next csv")
                                            continue
                                        else:
                                            s2_date = s2File.Date.tolist()
#                                            print("S2 is !empty will proceed")
#                                            print("length s2", len(s2_date))
                                    except:
                                        s2_date = []
#                                        print("no data in s2")
#                                        print("length s2", len(s2_date))
                                    csv3i = 0
                                    for csv3 in t2:
                                        if(os.path.basename(csv3)==s2common):
#                                            print("inif info s2common",os.path.basename(csv3),s2common)
                                            csv3i  += 1 
                                            try:
                                                infioFile  = pd.DataFrame()
                                                infioFile = pd.read_csv(csv3)
                                                if(infioFile.empty):
                                                    info_date = []
#                                                    print("info is empty will continue to next csv")
                                                else:
                                                    info_date = infioFile.Date.tolist()
#                                                    print("info is !empty will proceed")
#                                                    print("length info", len(info_date))
                                            except:
                                                info_date = []
#                                                print("no data in info")
#                                                print("length info", len(info_date))
                                                   
                                            s1_s2 = list(set(s2_date))
#                                            print(len(s1_s2))
                                            
                                            if(len(s1_s2) != len(info_date)):
                                                print("noteq!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                                if(not s2File.empty):
                                                    print("in if")
                                                    s2File.set_index('Date', inplace=True)
                                                    print("missing csv in info:", infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                                                    s2File.to_csv(infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                                                else:
                                                    print("in else")
                                                    print("missing csv in info:", infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                                                    s2File.to_csv(infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                        break                    


def update_uncommon_s1_folders():
    s1 = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/S1/*")
    s2 = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/S2/*")
    info = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/info/*")
    infoPath = "/home/mustafa/Projects/1000/micro_v2/info1/info/"
    
    s1_folder = []
    s2_folder=[]
    info_folder=[]
    for s1Csv in s1:
    #    print("s1Csv: ",s1Csv)
        s1_folder.append(os.path.basename(s1Csv))
        s11 = list(set(s1_folder))
        for s2Csv in s2:
    #        print("s2Csv:" ,s2Csv)
            s2_folder.append(os.path.basename(s2Csv))
            s21 = list(set(s2_folder))
            for infoCsv in info:
                info_folder.append(os.path.basename(infoCsv))
                s31 = list(set(info_folder))
                common1 = list(set(s11) & set(s21))
                common2 = list(set(common1) & set(s31))
                common_file = list(set(common1) & set(common2))    
                s1_common = list(set(s11) ^  set(s31))
                s2_common = list(set(s21) ^ set(s31))
                nc_common = list(set(s1_common + s2_common))
                for i in nc_common:
                    if((os.path.basename(s1Csv) ==i) and (os.path.basename(infoCsv) ==i)):
                        t = glob.glob(s1Csv+"/*.csv")
                        t2 = glob.glob(infoCsv+"/*.csv")
                        list1 = os.listdir(s1Csv)
                        s1_files = len(list1)
                        list3 = os.listdir(infoCsv)
                        info_files = len(list3)
                        c_files = list(set(list1) & set(list3))
                        nc_files1 = list(set(list1) ^ set(list3))
                        for common in c_files:
                            csv1i = 0
                            for csv1 in t:
                                if(os.path.basename(csv1)==common):
                                    print("inif s1 common",os.path.basename(csv1),common)
                                    csv1i  += 1
                                    try:
                                        s1File  = pd.DataFrame()
                                        print("csv1",csv1)
                                        s1File = pd.read_csv(csv1)
                                        if(s1File.empty):
                                            print("S1 is empty will continue to next csv")
                                            continue
                                        else:
                                            s1_date = s1File.Date.tolist()
                                            print("S1 is !empty will proceed")
                                            print("length s1", len(s1_date))
                                    except:
                                        s1_date = []
                                        print("no data in s1")
                                        print("length s1", len(s1_date))
                                    csv3i = 0
                                    for csv3 in t2:
                                        if(os.path.basename(csv3)==common):
                                            print("inif info common",os.path.basename(csv3),common)
                                            csv3i  += 1 
                                            try:
                                                infioFile  = pd.DataFrame()
                                                infioFile = pd.read_csv(csv3)
                                                if(infioFile.empty):
                                                    print("info is empty will continue to next csv")
                                                    continue
                                                else:
                                                    info_date = infioFile.Date.tolist()
                                                    print("info is !empty will proceed")
                                                    print("length info", len(info_date))
                                            except:
                                                info_date = []
                                                print("no data in info")
                                                print("length info", len(info_date))
                                                
                                            s1_s2 = list(set(s1_date))
                                            print(len(s1_s2))
                                            
                                            if(len(s1_s2) != len(info_date)):
                                                print("noteq!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                                s1File.set_index('Date', inplace=True)
                                                print("missing csv in info:", infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))
                                                s1File.to_csv(infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))  
                        for s1common in nc_files1:
                            csv1i = 0
                            for csv1 in t:
                                if(os.path.basename(csv1)==s1common):
                                    print("inif s1 common",os.path.basename(csv1),s1common)
                                    csv1i  += 1
                                    try:
                                        s1File  = pd.DataFrame()
                                        print("csv1",csv1)
                                        s1File = pd.read_csv(csv1)
                                        if(s1File.empty):
                                            print("S1 is empty will continue to next csv")
                                            continue
                                        else:
                                            s1File.set_index('Date', inplace=True)
                                            print("missing csv in info:", infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))
                                            s1File.to_csv(infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))
                                    except:
                                        s1File.set_index('Date', inplace=True)
                                        print("missing csv in info:", infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))
                                        s1File.to_csv(infoPath+os.path.basename(s1Csv)+"/"+os.path.basename(csv1))
                        break

def update_uncommon_s2_folders():
    s1 = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/S1/*")
    s2 = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/S2/*")
    info = glob.glob("/home/mustafa/Projects/1000/micro_v2/info1/info/*")
    infoPath = "/home/mustafa/Projects/1000/micro_v2/info1/info/"
    s1_folder = []
    s2_folder=[]
    info_folder=[]
    for s1Csv in s1:
    #    print("s1Csv: ",s1Csv)
        s1_folder.append(os.path.basename(s1Csv))
        s11 = list(set(s1_folder))
    for s2Csv in s2:
    #        print("s2Csv:" ,s2Csv)
        s2_folder.append(os.path.basename(s2Csv))
        s21 = list(set(s2_folder))
        for infoCsv in info:
            info_folder.append(os.path.basename(infoCsv))
            s31 = list(set(info_folder))
            s1_common = list(set(s11) ^  set(s31))
            s2_common = list(set(s21) ^ set(s31))
            com = list(set(s1_common) & set(s2_common))
            nc_common = list(set(s1_common) ^ set(s2_common))
            nc_common_s2 = list(set(nc_common) & set(s1_common))
            for j in nc_common_s2:
                if((os.path.basename(s2Csv) ==j) and (os.path.basename(infoCsv) ==j) ):
                    t1 = glob.glob(s2Csv+"/*.csv")
                    t2 = glob.glob(infoCsv+"/*.csv")
                    list2 = os.listdir(s2Csv)
                    s1_files = len(list2)
                    list3 = os.listdir(infoCsv)
                    info_files = len(list3)
                    c_files = list(set(list2) & set(list3))
                    nc_files1 = list(set(list2) ^ set(list3))
                    for common in c_files:
                        csv2i = 0
                        for csv2 in t1:
                            if(os.path.basename(csv2)==common):
                                print("inif common",os.path.basename(csv2),common)
                                csv2i  += 1
                                try:
                                    s2File  = pd.DataFrame()
                                    print("csv2",csv2)
                                    s2File = pd.read_csv(csv2)
                                    if(s2File.empty):
                                        print("S2 is empty will continue to next csv")
                                        continue
                                    else:
                                        s2_date = s2File.Date.tolist()
                                        print("S2 is !empty will proceed")
                                        print("length s2", len(s2_date))
                                except:
                                    s2_date = []
                                    print("no data in s2")
                                    print("length s2", len(s2_date))
                                csv3i = 0
                                for csv3 in t2:
                                    if(os.path.basename(csv3)==common):
                                        print("inif info common",os.path.basename(csv3),common)
                                        csv3i  += 1 
                                        try:
                                            infioFile  = pd.DataFrame()
                                            infioFile = pd.read_csv(csv3)
                                            if(infioFile.empty):
                                                print("info is empty will continue to next csv")
                                                continue
                                            else:
                                                info_date = infioFile.Date.tolist()
                                                print("info is !empty will proceed")
                                                print("length info", len(info_date))
                                        except:
                                            info_date = []
                                            print("no data in info")
                                            print("length info", len(info_date))
                                            
                                        s1_s2 = list(set(s2_date))
                                        print(len(s1_s2))
                                        
                                        if(len(s2_date) != len(info_date)):
                                            print("noteq!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                            try:
                                                if(not s2File.empty):
                                                    print("inside if")
                                                    s2File.set_index('Date', inplace=True)
                                                    print("missing csv in s2:", infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                                                    s2File.to_csv(infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                                                else:
                                                    print("inside else")
                                                    s2File.to_csv(infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                                            except:
                                                    s2File.to_csv(infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))  
                    for s2common in nc_files1:
                        csv2i = 0
                        for csv2 in t1:
                            if(os.path.basename(csv2)==s2common):
                                print("inif s2 common",os.path.basename(csv2),s2common)
                                csv2i  += 1
                                try:
                                    s2File  = pd.DataFrame()
                                    print("csv2",csv2)
                                    s2File = pd.read_csv(csv2)
                                    if(s2File.empty):
                                        print("S2 is empty will continue to next csv")
                                        continue
                                    else:
                                        s2File.set_index('Date', inplace=True)
                                        print("missing csv in info:", infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                                        s2File.to_csv(infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                                except:
                                    s2File.set_index('Date', inplace=True)
                                    print("missing csv in info:", infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                                    s2File.to_csv(infoPath+os.path.basename(s2Csv)+"/"+os.path.basename(csv2))
                    break
                   
update_common_folders()
update_common_s1_folders()
update_common_s2_folders()
update_uncommon_s1_folders()
update_uncommon_s2_folders()