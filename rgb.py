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

from utils import natural_keys, add_csv_extension

Version = "1.0.0"


# filepath - RGB data file, each line a tab-delimited series of four elements: depth, R, G, B
# returns list of RGB data rows, each a list of form [depth, R, G, B] 
def readSectionRGBFile(filepath, rgbFormat, averageRows=None, roundTo=None, reporter=None):
    srcfile = open(filepath, 'rU')
    df = pandas.read_csv(filepath, skiprows=rgbFormat.skiprows, skipinitialspace=True)
    srcfile.close()
    
    rgbRows = []
    if not averageRows:
        for tup in df.itertuples(): # itertuples() is significantly faster than iterrows()
            # each row is a tab-delimited blob of four elements: depth, red, green, and blue 
            # datalist = tup[1].split('\t') # (tup[0] is the index)
            datalist = rgbFormat.parse_row(tup)
            if roundTo is not None:
                datalist = [round(float(elt), roundTo) for elt in datalist]
            datalist.append(path.basename(filepath[:filepath.index('.')])) # append source section
            rgbRows.append(datalist)
    else:
        totals = {'depth':0, 'r':0, 'g':0, 'b':0}
        totalRows = len(df)
        for rowIndex, tup in enumerate(df.itertuples()):
            # datalist = [float(dat) for dat in tup[1].split('\t')] # (tup[0] is the index)
            datalist = rgbFormat.parse_row(tup)
            datalist = [float(d) for d in datalist]
            totals['depth'] += datalist[0]  
            totals['r'] += datalist[1]
            totals['g'] += datalist[2]
            totals['b'] += datalist[3]
            
            doAverage = (rowIndex + 1) % averageRows == 0  # at multiple of averageRows, compute average and add to rgbRows
            lastRow = rowIndex + 1 == totalRows  # file rows don't divide evenly by averageRows - average remainder  
            if doAverage or lastRow:
                rowCount = averageRows if doAverage else (rowIndex + 1) % averageRows
                if lastRow and reporter is not None:
                    reporter.report("Averaged last {} rows of file".format(rowCount), newline=False)
                if roundTo is not None:
                    averaged = [round(totals[key]/rowCount, roundTo) for key in ['depth','r','g','b']]
                else:
                    averaged = [totals[key]/rowCount for key in ['depth','r','g','b']]
                averaged.append(path.basename(filepath[:filepath.index('.')])) # append source section
                rgbRows.append(averaged)
                totals = {'depth':0, 'r':0, 'g':0, 'b':0}

    postMsg = "read {} rows".format(len(df)) + "" if averageRows is None else "; averaged to {} rows".format(len(rgbRows))
    reporter.report(postMsg)
         
    return rgbRows

def aggregateRGBFiles(rgbFormat, rgbFileDir, outputPath, averageRows, roundToDecimalPlaces, reporter):
    startTime = time.time()
    rgbRows = []
    totalFiles = 0
    totalRows = 0
    rgbFiles = sorted([f for f in listdir(rgbFileDir) if f[-4:] == '.csv'], key=natural_keys)
    for rgbFile in rgbFiles:
        reporter.report("Processing {} (file {}/{})...".format(rgbFile, totalFiles + 1, len(rgbFiles)))
        fileRgbRows = readSectionRGBFile(path.join(rgbFileDir, rgbFile), rgbFormat, averageRows, roundToDecimalPlaces, reporter)
        rgbRows.extend(fileRgbRows)
        totalFileRows = len(fileRgbRows) 
        totalRows += totalFileRows
        totalFiles += 1
    reporter.report("Creating goliath DataFrame...")
    rgbdf = pandas.DataFrame(rgbRows)
    
    outputPath = add_csv_extension(outputPath)
    reporter.report("Writing to {}...".format(outputPath), newline=False)
    rgbdf.to_csv(outputPath, index=False, header=False)
    reporter.report("done!\nWrote {} rows from {} files in {} seconds".format(totalRows, totalFiles, round(time.time() - startTime, 3)))
