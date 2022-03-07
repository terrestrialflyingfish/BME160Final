#!/usr/bin/env python3
# Name: Zia Truong (zitruong) 
# Group Members: Ryan Nguyen (rnguye20), Corey Du Val (cduval), Jafet Rodriguez La Paz (jrodr212), Jack Verhage (jverhage), Daniel Lozan (daalozan)
'''
Classes to help with analyzing nucleotide sequences.

NucParams: Analyzes codon and amino acid composition.
FastAReader: Parses .fa files and returns headers and their corresponding nucleotide sequences.
ProteinParams: Analyzes a protein sequence and returns properties of the protein such as isoelectric point, molecular weight, etc.
'''
import sys

class NucParams:
    """
    Calculate the number of nucleotides in a nucleotide sequence(s), its RNA codon composition, its amino acid composition, and the amino acid composition of the protein as integer counts.
 
    Author: Zia Truong
    Date: January 31, 2022
    Nucleotide sequence should be supplied as a string.
    The letters representing the nucleotides in the sequence can be in any case.
    Nucleotide sequences can be either RNA or DNA.
 
    initialized: inString, a string containing a nucleotide sequence
                   
    attributes: seq - string containing an uppercased version of inString's sequence
                rnaSeq - string containing seq's sequence but with only RNA nucleotides
                rnaCodonTable - dictionary containing all 64 codons and the single-letter code for the amino acid (or stop) they code for 
                dnaCodonTable - similar to rnaCodonTable, except with the DNA versions of the codons instead
                nucComp - dictionary with the counts of every valid nucleotide in the sequence
                rnaCodonCounts - dictionary containing the counts of every codon in the sequence (in the codon's RNA form)
                aaComp - dictionary containing the counts of amino acids in the instance of ProteinParam
    methods:  addSequence() - adds a new sequence to the NucParams object and updates all composition dictionaries accordingly
              aaComposition(inSeq) - returns dictionary with integer counts of all amino acids in the sequence given to it (inSeq
              nucComposition(inSeq) - returns dictionary with integer counts of all nucleotides in the sequence given to it
              codonComposition(inSeq) - returns dictionary with integer counts of all codons in the sequence given to it
              nucCount() - returns the total nucleotide count (sequence length) of the NucParam object's sequence(s)
              
    usage:
        exampleNuc = nucParams()
        for seq in seqFile:
            exampleNuc.addSequence(seq)
    """
    def __init__ (self, inString=''):
        '''
        Initialize a new instance of NucParams.
        '''
        #initialize and process sequence string
        self.seq = inString.upper()
        #create RNA version for codonComposition() and aaComposition()
        self.dnaSeq = self.seq.replace('U','T')
        self.rnaSeq = self.seq.replace('T','U')
        
        # RNA codon table
        self.rnaCodonTable = {
        # U
        'UUU': 'F', 'UCU': 'S', 'UAU': 'Y', 'UGU': 'C',  # UxU
        'UUC': 'F', 'UCC': 'S', 'UAC': 'Y', 'UGC': 'C',  # UxC
        'UUA': 'L', 'UCA': 'S', 'UAA': '-', 'UGA': '-',  # UxA
        'UUG': 'L', 'UCG': 'S', 'UAG': '-', 'UGG': 'W',  # UxG
        # C
        'CUU': 'L', 'CCU': 'P', 'CAU': 'H', 'CGU': 'R',  # CxU
        'CUC': 'L', 'CCC': 'P', 'CAC': 'H', 'CGC': 'R',  # CxC
        'CUA': 'L', 'CCA': 'P', 'CAA': 'Q', 'CGA': 'R',  # CxA
        'CUG': 'L', 'CCG': 'P', 'CAG': 'Q', 'CGG': 'R',  # CxG
        # A
        'AUU': 'I', 'ACU': 'T', 'AAU': 'N', 'AGU': 'S',  # AxU
        'AUC': 'I', 'ACC': 'T', 'AAC': 'N', 'AGC': 'S',  # AxC
        'AUA': 'I', 'ACA': 'T', 'AAA': 'K', 'AGA': 'R',  # AxA
        'AUG': 'M', 'ACG': 'T', 'AAG': 'K', 'AGG': 'R',  # AxG
        # G
        'GUU': 'V', 'GCU': 'A', 'GAU': 'D', 'GGU': 'G',  # GxU
        'GUC': 'V', 'GCC': 'A', 'GAC': 'D', 'GGC': 'G',  # GxC
        'GUA': 'V', 'GCA': 'A', 'GAA': 'E', 'GGA': 'G',  # GxA
        'GUG': 'V', 'GCG': 'A', 'GAG': 'E', 'GGG': 'G'  # GxG
        }
        #alphabetize rna codon table
        abcRNACodonTable = {pair[0]:pair[1] for pair in sorted(self.rnaCodonTable.items(), key=lambda x:x[0])}
        #group by amino acid
        self.rnaCodonTable = {pair[0]:pair[1] for pair in sorted(abcRNACodonTable.items(), key=lambda x:x[1])} #sorted sorts dictionary by the value given in the key parameter; x[0] sorts by keys, x[1] sorts by values

        #create DNA version of codon table
        self.dnaCodonTable = {key.replace('U','T'):value for key, value in self.rnaCodonTable.items()}
        
        #initialize sequence composition dictionaries
        self.nucComp = self.nucComposition(self.seq)
        self.rnaCodonCounts = self.codonComposition(self.rnaSeq)
        self.aaComp = self.aaComposition(self.rnaCodonCounts)
        
    def addSequence (self, inSeq):
        '''
        Add new sequences to the NucParams object, and update composition dictionaries accordingly.
        '''
        # uppercase content and make RNA copy
        inSeq = inSeq.upper()
        inRNASeq = inSeq.replace('T','U')
        inDNASeq = inSeq.replace('U','T')
        self.seq = self.seq + inSeq
        self.rnaSeq = self.rnaSeq + inRNASeq
        self.dnaSeq = self.dnaSeq + inDNASeq
        
        #get composition of new sequence
        newSeqCodonComp, newSeqNucComp = self.codonComposition(inRNASeq), self.nucComposition(inSeq)
        newSeqAaComp = self.aaComposition(newSeqCodonComp)

        #add new compositions to existing compositions
        self.rnaCodonCounts = {key:newSeqCodonComp.get(key, 0)+value for key,value in self.rnaCodonCounts.items()}
        self.nucComp = {key:newSeqNucComp.get(key, 0)+value for key,value in self.nucComp.items()}
        self.aaComp = {key:newSeqAaComp.get(key, 0)+value for key,value in self.aaComp.items()}
        return
    
    def aaComposition(self,codonCounts):
        '''
        Return a dictionary with the composition (counts) of all amino acids given a dictionary with the codon composition of a RNA sequence.
        '''
        aaComp = {}
        for key,value in codonCounts.items():
            #Assumption: Codons are given in their RNA versions
            aaComp[self.rnaCodonTable[key]] = aaComp.get(self.rnaCodonTable[key], 0) + value
        return aaComp
    
    def nucComposition(self, inSeq):
        '''
        Return a dictionary with the nucleotide composition (quantity of each nucleotide) of the input sequence.
        '''
        #count occurrences of each nucleotide in the input sequence
        nucComp = {nuc:inSeq.count(nuc) for nuc in ['A','C','T','G','U','N']}
        return nucComp
    
    def codonComposition(self, inSeq):
        '''
        Return a dictionary with the codon composition (quantity of each codon) of the input sequence.
        '''
        seqList = [inSeq[pos:pos+3] for pos in range(0,len(inSeq),3)]
        #Assumption: Nucleotide sequence is given in RNA format
        codonComp = {key:seqList.count(key) for key in self.rnaCodonTable.keys()}
        return codonComp
    
    def nucCount(self):
        '''Return the total number of nucleotides in the NucParams sequence(s)'''
        #sum all nucleotide counts to compute the total number of nucleotides
        return sum(self.nucComp.values())
    
class FastAreader :
    ''' 
    Define objects to read FastA files.
    
    instantiation: 
    thisReader = FastAreader ('testTiny.fa')
    usage:
    for head, seq in thisReader.readFasta():
        print (head,seq)
    '''
    def __init__ (self, fname=''):
        '''contructor: saves attribute fname '''
        self.fname = fname
            
    def doOpen (self):
        ''' Handle file opens, allowing STDIN.'''
        if self.fname == '':
            return sys.stdin   
        else:
            return open(self.fname)
        
    def readFasta (self):
        ''' Read an entire FastA record and return the sequence header/sequence'''
        header = ''
        sequence = ''
        
        with self.doOpen() as fileH:
            
            header = ''
            sequence = ''
            
            # skip to first fasta header
            line = fileH.readline()
            while not line.startswith('>') :
                line = fileH.readline()
            header = line[1:].rstrip()

            for line in fileH:
                if line.startswith ('>'):
                    yield header,sequence
                    header = line[1:].rstrip()
                    sequence = ''
                else :
                    sequence += ''.join(line.rstrip().split()).upper()

        yield header,sequence
        
class ProteinParam :
    """
    Calculate the number of amino acids in a protein, the protein's molecular weight, the 
    protein's molar extinction and mass extinction coefficients, the protein's isoelectric point, 
    and the amino acid composition of the protein as integer counts.
 
    Author: Zia Truong
    Date: January 24, 2022
    The amino acid sequence should be supplied as a string.
    The letters representing the amino acids can be in any case.
    Single-letter amino acid codes should be used, not three-letter codes or any other form of representation.
 
    initialized: protein, a string containing an amino acid sequence
    attributes: aa2chargePos, aa2chargeNeg - dictionaries containing the pKa of positively and negatively charged amino acids respectively
                aa2mw - dictionary containing the molecular weights of every amino acid
                mwH2O - the molecular weight of H2O
                aa2abs280 - dictionary with absorbances at 280nm of tyrosine, tryptophan, and cystine
                aaNterm, aaCterm - floats with pKa of the N-terminus and C-terminus respectively
                aaCounts - dictionary containing the counts of amino acids in the instance of ProteinParam
    methods:  aaCount() - returns total number of amino acids in the sequence
              aaComposition() - returns dictionary with integer counts of all amino acids in the protein
              _charge_() - returns the charge of the protein at the specified pH
              pI(sf=2) - returns isoelectric point of the protein to the specified precision
              molarExtinction(Cystine=True) - returns molar extinction coefficient of the protein at either oxidizing or reducing conditions
              massExtinction(Cystine=True) returns mass extinction coefficient of the protein at either oxidizing or reducing conditions
              molecularWeight() - returns the molecular weight of the protein
    """

    def __init__ (self, protein):
        """
        Initialize instance of ProteinParam.
        """
        self.aa2chargePos = {'K': 10.5, 'R':12.4, 'H':6}
        self.aa2chargeNeg = {'D': 3.86, 'E': 4.25, 'C': 8.33, 'Y': 10}
        self.aa2mw = {
        'A': 89.093,  'G': 75.067,  'M': 149.211, 'S': 105.093, 'C': 121.158,
        'H': 155.155, 'N': 132.118, 'T': 119.119, 'D': 133.103, 'I': 131.173,
        'P': 115.131, 'V': 117.146, 'E': 147.129, 'K': 146.188, 'Q': 146.145,
        'W': 204.225,  'F': 165.189, 'L': 131.173, 'R': 174.201, 'Y': 181.189
        }
        self.mwH2O = 18.015
        self.aa2abs280 = {'Y':1490, 'W': 5500, 'C': 125}
        self.aaNterm = 9.69
        self.aaCterm = 2.34
        #Assumption: input is a string
        self.protein = protein.upper() #ensures uppercase input
        #Assumption: amino acids are represented by their single-letter code
        self.aaCounts = {key:self.protein.count(key) for key in self.aa2mw.keys()} #define dictionary with amino acid counts

    def aaCount (self):
        """
        Returns the total number of amino acids in the protein.
        """
        return sum(self.aaCounts.values()) # self.aaCounts has the quantities of every amino acid, so summing the values gives the total amino acid count

    def pI (self, sf=2):
        """
        Finds the pH at which the isoelectric point of the protein is reached, and return it to the specified precision.
        """
        #Assumptions: there is a pH at which charge == 0, and charge always decreases with increasing pH
        ivMin,ivMax,pH = 0.0,14.0,7.0
        # binary search loop
        while ivMax - ivMin > 10**(-sf-1): #ensure loop stops when a high enough precision is reached
            pH = (ivMin + ivMax) / 2 #find center of current interval
            c = self._charge_(pH) # get charge at pH
            if c > 0:
                ivMin = pH #eliminate bottom half of interval
            else:
                ivMax = pH #eliminate top half of interval
        return float(format(pH, '.'+str(sf)+'f')) if self.aaCount() > 0 else 0.0 # format result to the specified precision; if else to account for the possibility of no amino acids

    def aaComposition (self) :
        """ 
        Returns a dictionary with the counts of every amino acid in the protein.
        """
        return self.aaCounts #already computed in self._init_

    def _charge_ (self,pH):
        """
        Returns the charge of the protein at the specified pH.
        """
        # defining these variables to reduce clunkiness
        p = self.aa2chargePos
        n = self.aa2chargeNeg
        counts = self.aaCounts
        nTerm, cTerm = self.aaNterm, self.aaCterm
        
        # loop for the total charge of the positively charged amino acids
        posSum = (10**nTerm/(10**nTerm+10**pH)) #not part of loop, so defined here
        for x in p.keys():
            posSum += (counts[x]*(10**(p[x])) / ((10**(p[x])) + (10**pH))) # as per formula
        
        # similar loop for negatively charged amino acids
        negSum = (10**pH/(10**cTerm+10**pH))
        for y in n.keys():
            negSum += ((counts[y]*(10**pH) / (10**(n[y]) + 10**pH)))
            
        return posSum - negSum

    def molarExtinction (self, Cystine=True):
        """
        Returns molar extinction coefficient of the protein under either oxidizing or reducing conditions 
        (Cystine=True represents oxidizing, Cystine=False represents reducing).
        """
        meCoeff = self.aaCounts["W"]*self.aa2abs280["W"] + self.aaCounts["Y"]*self.aa2abs280["Y"] #as per formula
        return meCoeff + (self.aaCounts["C"]*self.aa2abs280["C"]) if Cystine else meCoeff #only count the absorbance of cystine when conditions are oxidizing

    def massExtinction (self, Cystine=True):
        """
        Returns mass extinction coefficient of the protein under either oxidizing or reducing conditions
        (Cystine=True represents oxidizing, Cystine=False represents reducing).
        """
        myMW = self.molecularWeight()
        return self.molarExtinction(Cystine) / myMW if myMW else 0.0  #avoid having to recompute molar extinction coefficient

    def molecularWeight (self):
        """
        Returns molecular weight of the protein.
        """
        aaWeights = [value*self.aa2mw[key] for key,value in self.aaCounts.items()] #sum molecular weights of amino acids
        return sum(aaWeights)-(self.aaCount()-1)*self.mwH2O if self.aaCount() > 0 else 0.0 #if else to avoid returning a molecular weight when there are no amino acids