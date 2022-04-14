'''
Created on April 14, 2022

@author: bgrivna

RGB data formats and parsing logic
'''

class SectionRGBFormat:
    def __init__(self, name, desc, skiprows, parser):
        self.name = name
        self.desc = desc
        self.skiprows = skiprows
        self.parser = parser

    def parse_row(self, tuple):
        return self.parser(tuple)

# Depth, R, G, B values are in tuple element 1, separated by tabs.
# Always ignore element 0 of the tuple (the pandas index).
def tabSeparatedParser(tuple):
    datalist = tuple[1].split('\t')
    return datalist

# Depth, R, G, B values are separate elements of the tuple.
# Always ignore element 0 of the tuple (the pandas index).
# If the tuple contains six elements, assume element 1 is the
# measurement count and ignore.
def imageJParser(tuple):
    # some files include a sequence as the first column, some don't
    assert 5 <= len(tuple) <= 6, f"Unexpected tuple {tuple}"
    if len(tuple) == 5:
        offset = 1 # skip pandas index
    else:
        offset = 2 # skip pandas index and measurement count column
    datalist = [tuple[offset], tuple[offset+1], tuple[offset+2], tuple[offset+3]]
    return datalist

def getFormats():
    ps = [
        SectionRGBFormat("Original", "Depth and RGB values separated by tabs in a single cell", 7, tabSeparatedParser),
        SectionRGBFormat("ImageJ", "Depth, R, G, B in separate cells; ignore measurement sequence in column 1 if present", 0, imageJParser)
    ]
    return ps