import numpy as np
import tmm
import matplotlib.pyplot as plt
import csv
from scipy.interpolate import interp1d
#import pandas as pd

# This whole thing uses microns for length

degree = np.pi/180
inc_angle = 0.*degree

class Layer:
    """ 
    I am a layer class for organizing data for each layer. I should make constructing stacks easier in the future and reduce possible mistakes
    """
    def __init__(self, thickness, fname_root):
        self.d = thickness
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
        
        
        
num_lams = 500
lams = np.linspace(0.3,2.5,num=num_lams)

Glass = Layer(4000,'Rubin-clear')
TiO2 = Layer(0.05,'Siefke')
AZO = Layer(0.2,'Treharne')
MAPI = Layer(0.1,'Phillips')
ITO = Layer(0.2,'Moerland')
ZnO = Layer(0.05,'Stelling')
PVP = Layer(1500,'Konig')

#Glass = Layer(4000,1.+0.0j)
#FTO = Layer(0.2,1.2+0.02j)

layers = [Glass,ITO,TiO2,MAPI,ZnO,AZO,PVP,Glass]

thicks = [tmm.inf]
nks = [1]
for layer in layers:
    thicks.append(layer.d)
    nks.append(layer.nk(1.1))
thicks.append(tmm.inf)
nks.append(1)
    

print(thicks)

outstuffs = []

Ts = []
Rfs = []
Rbs = []

for lam in lams:
    
    front_spol = tmm.coh_tmm('s',nks,thicks,inc_angle,lam)
    front_ppol = tmm.coh_tmm('p',nks,thicks,inc_angle,lam)
    back_spol = tmm.coh_tmm_reverse('s',nks,thicks,inc_angle,lam)
    back_ppol = tmm.coh_tmm_reverse('p',nks,thicks,inc_angle,lam)
    
    Rfs.append( (front_spol['R']+front_ppol['R']) / 2.)
    Rbs.append( (back_spol['R']+back_ppol['R']) / 2.)
    Ts.append( (front_spol['T']+front_ppol['T']) / 2. )



plt.figure()
plt.plot(lams,Rfs,color='magenta',marker=None,label="$R_f$")
plt.plot(lams,Ts,color='green',marker=None,label="$T$")
plt.xlabel('wavelength, $\mu$m')
plt.legend()
plt.show()

# will need this later:
# def absorp_in_each_layer(coh_tmm_data):
# note: input is output from coh_tmm()

