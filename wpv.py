import csv
from scipy.interpolate import interp1d
import numpy as np

class Layer:
    """ 
    I am a layer class for organizing data for each layer. I should make constructing stacks easier in the future and reduce possible mistakes
    """
    def __init__(self, thickness, fname_root, i_or_c):
        self.d = thickness
        self.i_or_c = i_or_c
        #self.nk = 1.0
        
        """
        next we will unpack n and k data from a csv file and turn it into a callable interpolation function
        """
        matfilename = 'Data/' + fname_root + '.csv'
        lct = 0
        bothdat = []
        with open(matfilename, newline='') as csvfile:
            rawdat = csv.reader(csvfile, delimiter=' ')
            for row in rawdat:
                lct += 1
                if row:
                    bothdat.append(row[0])
                    if 'k' in row[0]:
                        kstart = lct
            lct = 1
            nlams = []
            ns = []
            klams = []
            ks = []
            for line in bothdat:
                if lct < kstart-1:
                    if 'n' not in line:
                        nlams.append(float(line.split(',')[0]))
                        ns.append(float(line.split(',')[1]))
                else:
                    if 'k' not in line:
                        #print(line)
                        klams.append(float(line.split(',')[0]))
                        ks.append(float(line.split(',')[1]))
                lct += 1
        nlams = np.array(nlams)
        ns = np.array(ns)
        #print(nlams)
        klams = np.array(klams)
        ks = np.array(ks)
        #print(klams)
        
        '''
        plt.figure()
        plt.plot(nlams,ns)
        plt.plot(klams,ks)
        plt.show()
        '''
        
        self.n = interp1d(nlams,ns,fill_value="extrapolate")
        self.k = interp1d(klams,ks,fill_value="extrapolate")
        
    def nk(self,lam):
        return complex(self.n(lam),self.k(lam))
  
