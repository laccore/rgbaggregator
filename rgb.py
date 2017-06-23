'''
Created on Jun 22, 2017

@author: bgrivna

Gather data from individual sections' RGB data files and combine
them into a single CSV file with an additional column indicating the source
section for each row of data.
'''

from os import path, listdir
import time

import pandas

# filepath - RGB data file, each line a tab-delimited series of four elements: depth, R, G, B
# returns list of RGB data rows, each a list of form [depth, R, G, B] 
def readSectionRGBFile(filepath):
    srcfile = open(filepath, 'rU')
    df = pandas.read_csv(filepath, skiprows=7, skipinitialspace=True)
    srcfile.close()
    
    rgbRows = []
    for tup in df.itertuples(): # itertuples() is significantly faster than iterrows()
        # each row is a tab-delimited blob of four elements: depth, red, green, and blue 
        datalist = tup[1].split('\t') # (tup[0] is the index)
        datalist.append(path.basename(filepath[:filepath.index('.')])) # append source section
        rgbRows.append(datalist)
         
    return rgbRows

def aggregateRGBFiles(rgbFileDir, outputPath, reporter):
    startTime = time.time()
    rgbRows = []
    totalFiles = 0
    totalRows = 0
    rgbFiles = [f for f in listdir(rgbFileDir) if f[-4:] == '.csv']
    for rgbFile in rgbFiles:
        reporter.report("Processing {} (file {}/{})...".format(rgbFile, totalFiles + 1, len(rgbFiles)), newline=False)
        fileRgbRows = readSectionRGBFile(path.join(rgbFileDir, rgbFile))
        rgbRows.extend(fileRgbRows)
        totalFileRows = len(fileRgbRows) 
        totalRows += totalFileRows
        reporter.report("read {} rows".format(totalFileRows))
        totalFiles += 1
    rgbdf = pandas.DataFrame(rgbRows)
    
    reporter.report("Writing to {}...".format(outputPath), newline=False)
    rgbdf.to_csv(outputPath, index=False, header=False)
    reporter.report("done!\nWrote {} rows from {} files in {} seconds".format(totalRows, totalFiles, round(time.time() - startTime, 3)))
