'''
Created on Jun 20, 2017

@author: bgrivna

Command-line main module for rgbaggregator
'''

import sys

import rgb

class StdoutReporter():
    def report(self, string, newline=True):
        sys.stdout.write(string)
        if newline:
            sys.stdout.write("\n")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "usage: python rgbaggregator.py <dir containing RGB files> <destination file for combined RGB data>"
        print "NOTE: script will attempt to consume *any* CSV file in dir - files with unexpected format will result in sadness"
        exit(-1)
        
    rgbFileDir = sys.argv[1]        
    outputPath = sys.argv[2]
    reporter = StdoutReporter()

    rgb.aggregateRGBFiles(rgbFileDir, outputPath, reporter)