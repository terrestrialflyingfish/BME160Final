#!/usr/bin/env python3
# Group Members: Jack Verhage (jverhage), Zia Truong (zitruong)


class PrintColor:

    '''
    Take in an input of capital amino acid one letter characters
    and outputs them as a colored string with red being hydrophobic, green
    being neutral, and blue being hydrophilic

    '''    

    def printRed(self):
        ''' Prints the red characters by setting the color to red, printing,
        and then setting the color back to normal. '''
        
        print('\033[0;0;41m', end = '')
        print(self, end = '')
        print('\033[0;0;0m', end = '')
        
    def printBlue(self):
        ''' Prints the blue characters by setting the color to red, printing,
        and then setting the color back to normal. '''
        
        print('\033[0;0;44m', end = '')
        print(self, end = '')
        print('\033[0;0;0m', end = '')
        
    def printGreen(self):
        ''' Prints the green characters by setting the color to red, printing,
        and then setting the color back to normal. '''
        
        print('\033[0;0;42m', end = '')
        print(self, end = '')
        print('\033[0;0;0m', end = '')
        
    def printStrand(string):
        ''' Prints the characters by iterating through the input string and
        printing the characters as red, green, or blue if they are contained in
        the hydrophobic, neutral, or hydrophilic lists. '''
        
        hydrophobic = ['I', 'V', 'L', 'F', 'C', 'M', 'A', 'W']
        neutral = ['G', 'T', 'S', 'Y', 'P', 'H']
        hydrophilic = ['N', 'D', 'Q', 'E', 'K', 'R']
        
        for x in string:        # Iterates through the string and prints the
                                # characters in the appropriate colors
            if x in hydrophobic:
                PrintColor.printRed(x)
            if x in neutral:
                PrintColor.printGreen(x)
            if x in hydrophilic:
                PrintColor.printBlue(x)
            
