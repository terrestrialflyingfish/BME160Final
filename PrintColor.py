# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


# =============================================================================
# 
# 
# print('\033[1;;41mCHEESY')
# print('\033[0;0;0m', end = '')
# 
# print('hello')
# print('\033[1;;42mCHEESY')
# print('\033[1;;43mCHEESY')
# print('\033[1;;44mCHEESY')
# print('\033[1;;45mCHEESY')
# print('\033[1;;46mCHEESY')
# print('\033[1;;47mCHEESY')
# 
# 
# 
# print('\033[1;;41m', end = '')
# 
# print('{}'.format('zzz'))
# print('whatever')
# =============================================================================





class PrintColor:

    def printRed(self):
        print('\033[0;0;41m', end = '')
        print(self, end = '')
        print('\033[0;0;0m', end = '')
        
    def printBlue(self):
        print('\033[0;0;44m', end = '')
        print(self, end = '')
        print('\033[0;0;0m', end = '')
        
    def printGreen(self):
        print('\033[0;0;42m', end = '')
        print(self, end = '')
        print('\033[0;0;0m', end = '')
        
    def printStrand(string):
        hydrophobic = ['I', 'V', 'L', 'F', 'C', 'M', 'A', 'W']
    
        neutral = ['G', 'T', 'S', 'Y', 'P', 'H']
    
        hydrophilic = ['N', 'D', 'Q', 'E', 'K', 'R']
        for x in string:
            if x in hydrophobic:
                PrintColor.printRed(x)
            if x in neutral:
                PrintColor.printGreen(x)
            if x in hydrophilic:
                PrintColor.printBlue(x)
            

# =============================================================================
# print('aaa')
# x = 'zzz'
# PrintColor.printRed(x)
# PrintColor.printBlue(x)
# PrintColor.printGreen(x)
# print('aaa')
# =============================================================================

# =============================================================================
# 
# strand = 'IVFCMAWNDQEGTSYP'
# 
# PrintColor.printStrand(strand)
# 
# =============================================================================
