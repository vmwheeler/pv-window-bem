import csv
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt

class Layer:
    """ 
    I am a layer class for organizing data for each layer. I should make constructing stacks easier in the future and reduce possible mistakes
    """
    
    def __init__(self, thickness, fname_root, i_or_c,**kwargs):
        self.d = thickness
        self.i_or_c = i_or_c
        #self.nk = 1.0
        self.datasource = fname_root
        
        if kwargs.get('onecol'):
            print('dumb data')
            self.get_dumb_data()
        else:
            self.get_sensible_data()
        
    
    
    def get_dumb_data(self):
        
        matfilename = 'Data/' + self.datasource + '.csv'
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
        
        self.n = interp1d(nlams,ns,fill_value="extrapolate")
        self.k = interp1d(klams,ks,fill_value="extrapolate")
        
        
    
        

        
    def get_sensible_data(self):
        """
                next we will unpack n and k data from a csv file and turn it into a callable interpolation function
        """
        
        matfilename = 'Data/' + self.datasource + '.csv'
        testdat = np.genfromtxt(matfilename,delimiter=',',skip_header=1)
        
        nlams = testdat[:,0]
        ns = testdat[:,1]
        ks = testdat[:,2]
        
        self.n = interp1d(nlams,ns,fill_value="extrapolate")
        self.k = interp1d(nlams,ks,fill_value="extrapolate")
        
        
    def nk(self,lam):
        return complex(self.n(lam),self.k(lam))
    
    def plotnk(self,lams):
        
        plt.figure()
        plt.plot(lams, self.n(lams),label='n')
        plt.plot(lams, self.k(lams),label='k')
        plt.title(self.datasource)
        plt.legend()
        plt.show()
                 
  
