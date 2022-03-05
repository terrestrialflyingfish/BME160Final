import numpy as np
import pandas as pd


class dataGen:
    def _init_():
        self.a = ""

    def padData(self,arr):
        """make sure all lists are same length"""
        lens = [len(kj) for kj in arr]
        maxLength = max(lens)
        minLength = min(lens)
   
        return [v + [0] * (maxLength - len(v)) for v in arr]

    def stdData(self,arr):
        z = np.array(arr)
        mn = np.mean(z, axis=0)
        st = np.std(z, axis=0)
        zz = (z - mn) / st
        np.nan_to_num(zz, copy=False)
        return zz

    def hydro(self,seq, l=11):
        hydroDict = {
            "A": 1.8,
            "G": -0.4,
            "M": 1.9,
            "S": -0.8,
            "C": 2.5,
            "H": -3.2,
            "N": -3.5,
            "T": -0.7,
            "D": -3.5,
            "I": 4.5,
            "P": -1.6,
            "V": 4.2,
            "E": -3.5,
            "K": -3.9,
            "Q": -3.5,
            "W": -0.9,
            "F": 2.8,
            "L": 3.8,
            "R": -4.5,
            "Y": -1.3,
        }
        k = []
        hydropathies = [hydroDict[aa] for aa in seq]
        for x in range(0, len(seq), l):
            frag = hydropathies[x : x + l]
            k.append(sum(frag) / len(frag))

        avg = sum(hydropathies) / len(hydropathies)
        return k

    def charge(self,aa, pH=7):
        # info from http://chem.ucalgary.ca/courses/351/Carey5th/Ch27/ch27-1-4-2.html
        infoDict = {
            "A": (2.34, 9.69, 0, 6.00),
            "G": (2.34, 9.60, 0, 5.97),
            "M": (2.28, 9.21, 0, 5.74),
            "S": (2.21, 9.15, 0, 5.68),
            "C": (1.96, 8.18, 0, 5.07),
            "H": (1.82, 9.17, 6.00, 7.59),
            "N": (2.02, 8.80, 0, 5.41),
            "T": (2.09, 9.10, 0, 5.60),
            "D": (1.88, 9.60, 3.65, 2.77),
            "I": (2.36, 9.60, 0, 6.02),
            "P": (1.99, 10.60, 0, 6.30),
            "V": (2.32, 9.62, 0, 5.96),
            "E": (2.19, 9.67, 4.25, 3.22),
            "K": (2.18, 8.95, 10.53, 9.74),
            "Q": (2.17, 9.13, 0, 5.65),
            "W": (2.83, 9.39, 0, 5.89),
            "F": (1.83, 9.13, 0, 5.48),
            "L": (2.36, 9.60, 0, 5.98),
            "R": (2.17, 9.04, 12.48, 10.76),
            "Y": (2.20, 9.11, 0, 5.66),
        }

        t = infoDict[aa]
        pH = int(pH)
        coo = -1 / (1 + (10 ** (t[0] - pH)))
        nh = 1 / (1 + (10 ** (pH - t[1])))
        sc = 0 if t[2] == 0 else -1 / (1 + (10 ** (t[2] - pH)))if t[2] < 7 else 1 / (1 + (10 ** (pH - t[2])))
        return coo + nh + sc

    def phs(self, seq, pH=7, l=1):
        charges = [self.charge(aa, pH) for aa in seq]
        k = []
        l = int(l)
        for x in range(0, len(seq), l):
            frag = charges[x : x + l]
            k.append((sum(frag) / len(frag)))
        return k

    def pca(self,data):
        graphData = self.padData(data)
        print(graphData)
        X = self.stdData(graphData)
        covariance_matrix = np.cov(X.T)
        eigen_values, eigen_vectors = np.linalg.eig(covariance_matrix)
        projection_matrix = (eigen_vectors.T[:][:2]).T
        X_pca = X.dot(projection_matrix)
        labels = [str(a + 1) for a in range(len(X_pca[:, 0]))]
        x = X_pca[:, 0]
        y = X_pca[:, 1]
        return x, y
