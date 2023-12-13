# Code developed and shared by:
# Vasilis Oikonomou
# Joshua Abbott
# Jessie Salas

import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import re
from random import random
import numpy as np
from matplotlib import gridspec
import warnings
import string
import os
from scipy import spatial 
warnings.filterwarnings('ignore')

def readNamingData(namingDataFilePath):
    """
    Read all of namingDataFilePath into a dictionary, and return it.  Assumes data file follows WCS format:
    language number\tspeaker number\tchip number\tlanguage term for chip\n

    Parameters
    ----------
    namingDataFilePath : string
        The path (and filename, with the extension) to read the WCS-formatted color naming data from.
 

    Returns
    -------
    namingData : dictionary
    	A hierarchical dictionary: namingData[languageNumber][speakerNumber][chipNumber] = languageTerm


    Example Usage:
    --------------
    import wcsFunctions as wcs
    namingDictionary = wcs.readNamingData('./WCS-Data/term.txt')

    """
    namingData = {}  # empty dict
    fileHandler = open(namingDataFilePath,'r')

    for line in fileHandler:              			# for each line in the file
        lineElements = line.split()     			# lineElements are denoted by white space
        
        # WCS format for naming data from term.txt:
        # language number\tspeaker number\tchip number\tlanguage term for chip

        languageNumber = int(lineElements[0])    	# 1st element is language number, make it an int
        speakerNumber = int(lineElements[1])  		# 2nd is speaker number, make int
        chipNumber = int(lineElements[2])     		# 3rd is chip number, make int
        languageTerm = lineElements[3]           	# 4th is languageTermegory assignment (term), keep string
        
        if not (languageNumber in namingData.keys()):    						# if this language isn't a key in the namingData dict
            namingData[languageNumber] = {}              							# then make it one, with its value an empty list
        if not (speakerNumber in namingData[languageNumber].keys()):   			# if this speaker isn't a key in the languageNumber dict
            namingData[languageNumber][speakerNumber] = {}             				# then make it one, with its value an empty list
        
        namingData[languageNumber][speakerNumber][chipNumber] = languageTerm  	# fill in these empty lists to make a GIANT namingData dictionary
                                            									# where each entry looks like this: {1: {1: {1: 'LB'}}
                                            									# and thus namingData[1][1][1] returns string 'LB'
    
    fileHandler.close()				# close file after reading it in, for neatness
    return namingData 				# return the dict


def readChipData(chipDataFilePath):
    """
    Read all of chipDataFilePath into two dictionaries, one maps from row/column code to WCS chip number,
	the other maps in the other direction.  Assumes data file follows WCS format:
    chip number\tWCS grid row letter\tWCS grid column number\tWCS grid rowcol abbreviation\n

    Parameters
    ----------
    chipDataFilePath : string
        The path (and filename, with the extension) to read the WCS-formatted chip data from.
 

    Returns
    -------
    cnum : dictionary
    	cnum[row/column abbreviation] = WCS chipnumber, thus cnum maps from row/col designation to chip number

    cname : a dictionary
    	cname[WCS chipnumber] = row letter, column number (a tuple), thus cname maps from chip number to row/col designation


    Example Usage:
    --------------
    import wcsFunctions as wcs
    cnumDictionary, cnameDictionary = wcs.readChipData('./WCS-Data/chip.txt')

    """
    
    cnum = {}    # empty dict to look up number given row/column designation
    cname = {}   # empty dict to look up row/column designation given number
    fileHandler = open(chipDataFilePath, 'r')    # open file for reading
    for line in fileHandler:               # for each line in the file
        lineElements = line.split()      # elements are denoted by white space
        chipnum = int(lineElements[0])   # 1st element is chip number, make it an int
        RC = lineElements[3]             # 4th is row/column designation, leave str (NB dictionaries don't exactly reverse each other)
        letter = lineElements[1]         # 2nd is the letter (row) designation
        number = str(lineElements[2])    # 3rd is the number (column) designation, make string so we can combine it with letter as a tuple in cname dict

        # cnum[rowcol] maps from row/column designation to chip number
        cnum[RC] = chipnum
        # cname[chipnum] maps from chip number to row/column designation (a tuple)
        cname[chipnum] = letter,number
        
    fileHandler.close()

    return cnum,cname            # return both dicts


# +
def readDictFile(filename):
    data = {}
    for i in range(1,111):
        data[i] = []
    with open(filename, 'r') as file:
        next(file)  # Skip the header
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) >= 4:
                lnum, tnum, tran, wcsc = int(parts[0]), int(parts[1]), parts[2], parts[3]
                data[lnum].append((tran, wcsc))
    return data

def translate(data, lnum, wcsc):
    if lnum in data and isinstance(data[lnum], list):
        for pair in data[lnum]:
            if pair[1] == wcsc:
                return pair[0]
    return None  # Return None if the key or subkey is not found


# -

def generate_random_values(ar):
    """Takes in an array of terms and returns a dictionary that maps terms to random values between 0 and 1"""
    d = {}
    for term in ar:
        d[term] = random()
    return d

def map_array_to(ar, d):
    """Maps an array of terms into an array of random values given the dictionary created by the above function"""
    return [d[i] for i in ar]

# uv_dict = {}
# counter = 0
# currLat = ''
# lat = 0
# total = 0
# for filename in os.listdir('./WCS_data_core/L3'):
#     f = os.path.join('./WCS_data_core/L3', filename)
#     if f != './WCS_data_core/L3/.ipynb_checkpoints':
#         total += 1
#         fileHandler = open(f,'r')
#         next(fileHandler)
#         next(fileHandler)
#         next(fileHandler)
#         for line in fileHandler:
#             counter+= 1
#
#             if 1 <= counter <= 12:
#                 if counter < 12:
#                     currLat += line.strip()
#
#                 else:
#                     currLat += line.strip(' ').split()[0]
#                     lat = float(line.strip('=').split()[-1])
#                     long = -179.375
#                     for i in range(288):
#                         if (lat, long) in uv_dict:
#                             uv_dict[(lat, long)] += int(currLat[i*3:i*3+3])
#                         else:
#                             uv_dict[(lat, long)] = int(currLat[i*3:i*3+3])
#                         long += 1.25  
#
#                     counter = 0
#                     currLat = ''
# for i in uv_dict:
#     uv_dict[i] = int(uv_dict[i]) / total


# print(uv_dict)

# +
from bisect import bisect_left

def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before
# -

# coord = {}
# cat = {}
# filename = './WCS_data_core/cog260 color data.txt'
#
# with open(filename, 'r') as file:
#     next(file)
#     for line in file:
#         lineElements = line.split()  
#         coord[int(lineElements[0])] = (float(lineElements[3]),float(lineElements[4]))
#         cat[int(lineElements[0])] = lineElements[2]
#
#         
#
# lat_list = []
# long_list = []
#
# for i in range(180):
#     lat_list.append(-89.5 + i)
# for i in range(288):
#     long_list.append(-179.375 + i* 1.25)
#
#
# cleaned_coord = {}
# for i in coord:
#     cleaned_coord[i] = [0,0]
#     cleaned_coord[i][0] = take_closest(lat_list, coord[i][0])
#     cleaned_coord[i][1] = take_closest(long_list, coord[i][1])
#
# print(cleaned_coord)
# sum_uv = {}
# for i in cleaned_coord:
#     sum_uv[tuple(cleaned_coord[i])] = uv_dict[tuple(cleaned_coord[i])]
# print(sum_uv)
# data = {}
# for i in coord:
#     data[i] = uv_dict[tuple(cleaned_coord[i])]
#
#
# cat0 = {}
# cat1 = {}
# for j in data:
#     if cat[j] == 'yes':
#         cat1[j] = data[j]
#     else:
#         cat0[j] = data[j]
# print(cat0)
#
# m0 = np.median(list(cat0))
# m1 = np.median(list(cat1))
# correctness = []
# for i in cat0:
#     med0 = list(cat0.values())
#     med0.remove(cat0[i])
#     m0 = np.median(med0)
#     
#         # Calculate the distance of the test point to their respective median
#     d0 = abs(m0 - cat0[i])
#     d1 = abs(m1 - cat0[i])
#     
#     if d0 < d1:
#         correctness.append(True)
#     else:
#         correctness.append(False)
#         
# for j in cat1:
#     med1 = list(cat1.values())
#     med1.remove(cat1[j])
#     m1 = np.median(med1)
#     
#         # Calculate the distance of the test point to their respective median
#     d0 = abs(m0 - cat1[j])
#     d1 = abs(m1 - cat1[j])
#     
#     if d0 < d1:
#         correctness.append(False)
#     else:
#         correctness.append(True)
#     
# print(correctness)
# print(cat)
# print(sum(correctness) / len(correctness))
#
#


# coord = {}
# cat = {}
# filename = './WCS_data_core/cog260 color data.txt'
#
# analysisData = {}
# with open(filename, 'r') as file:
#     next(file)
#     for line in file:
#         lineElements = line.split()  
#         analysisData[int(lineElements[0])] = [float(lineElements[3]),
#                                           float(lineElements[4]), lineElements[2], 0]
#
# print(analysisData)


# lat_list = []
# long_list = []
#
# for i in range(180):
#     lat_list.append(-89.5 + i)
# for i in range(288):
#     long_list.append(-179.375 + i* 1.25)
#
# cleaned_coord = {}
# for i in analysisData:
#     lat = analysisData[i][0]
#     long = analysisData[i][1]
#     cat = analysisData[i][2]
#     analysisData[i] = [take_closest(lat_list, lat), take_closest(long_list, long), cat, 0]
#
# print(analysisData)

# data = {}
# for i in analysisData:
#     analysisData[i][3] = uv_dict[(analysisData[i][0], analysisData[i][1])]
# print(analysisData)

#
#
# cat0 = {}
# cat1 = {}
# for i in range(1,111):
#     if analysisData[i][2] == 'yes':
#         cat1[i] = analysisData[i][3]
#     else:
#         cat0[i] = analysisData[i][3]
#
# print(cat0)
# m0 = np.median(list(cat0))
# m1 = np.median(list(cat1))
# correctness = []
# for i in cat0:
#     med0 = list(cat0.values())
#     med0.remove(cat0[i])
#     m0 = np.median(med0)
#     
#     # Calculate the distance of the test point to their respective median
#     d0 = abs(m0 - cat0[i])
#     d1 = abs(m1 - cat0[i])
#     
#     if d0 < d1:
#         correctness.append(True)
#     else:
#         correctness.append(False)
#         
# for j in cat1:
#     med1 = list(cat1.values())
#     med1.remove(cat1[j])
#     m1 = np.median(med1)
#     
#         # Calculate the distance of the test point to their respective median
#     d0 = abs(m0 - cat1[j])
#     d1 = abs(m1 - cat1[j])
#     
#     if d0 < d1:
#         correctness.append(False)
#     else:
#         correctness.append(True)
#     
# correct = sum(correctness) / len(correctness)
# print(correct)


# exemplar = []
# exemplar_correctness = []
# for test_point in analysisData:
#     total0 = 0
#     for vec in cat0:
#         dist = abs(vec - test_point)
#         sim = np.exp(-(dist**2))
#         total0 += sim
#         
#     total1 = 0
#     for vec in cat1:
#         dist = abs(vec - test_point)
#         sim = np.exp(-(dist**2))
#         total1 += sim
#         
#     c0 = total0 / len(cat0)
#     c1 = total1 / len(cat1)
#     
#     if c0 > c1:
#         # cat 0 - no
#         exemplar.append('no')
#         exemplar_correctness.append(analysisData[test_point][2] == 'no')
#         
#     else:
#         # cat 1 - yes
#         exemplar.append('yes')
#         exemplar_correctness.append(analysisData[test_point][2] == 'yes')
#         
# correct = sum(exemplar_correctness) / len(exemplar_correctness)
# print(correct)

# # Create a figure
# fig = plt.figure(figsize=(20, 1))
#
# # Plot markers for cat0 with flipped axes
# plt.scatter(cat0.values(), list(cat0.keys()), c='green', s=200)
#
# # Plot markers for cat1 with flipped axes
# plt.scatter(cat1.values(), list(cat1.keys()), c='blue', s=200, label = "Yes")
#
#
# plt.xlabel("UV-B incidence")
# # Show the plot
# plt.show()
# print(len(cat0))
# print(len(cat1))
#
# norm_cat0 = [float(i)/sum(cat0.values()) for i in cat0.values()]
# norm_cat1 = [float(i)/sum(cat1.values()) for i in cat1.values()]
# print(sum(norm_cat1))

# plt.subplot(1,2,1)
#
# plt.hist(cat0.values(), range = [0, 400], bins = 20, edgecolor = "black", alpha = 0.2)
# plt.subplot(1,2,2)
# plt.hist(cat1.values(),  range = [0, 400], bins = 20, edgecolor = "black")
# plt.show()


# plt.hist(cat0.values(), range = [200, 450], bins = 20, edgecolor = "black", alpha = 0.2, density = True)
#
# plt.hist(cat1.values(), range = [200, 450], bins = 20, edgecolor = "black", alpha = 0.2, density = True)
# plt.legend(["No distinct terms for blue and green", "Distinct terms for blue and green"])
# plt.show()




