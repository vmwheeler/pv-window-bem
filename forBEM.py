import numpy as np
import tmm
import matplotlib.pyplot as plt
#import pandas as pd

# This whole thing uses microns for length

degree = np.pi/180
inc_angle = 35.*degree

class Layer:
    """ 
    I am a layer class for organizing data for each layer. I should make constructing stacks easier in the future and reduce possible mistakes
    """
    def __init__(self, thickness, mat_fname):
        self.d = thickness
        self.nk = 1.0
        
        print(mat_fname)
        moop
  
num_lams = 200
lams = np.linspace(0.3,2.5,num=num_lams)

Glass = Layer(4000,'Rubin-clear')
#Glass = Layer(4000,1.+0.0j)
#FTO = Layer(0.2,1.2+0.02j)

layers = [Glass,FTO,Glass]

thicks = [tmm.inf]
nks = [1]
for layer in layers:
    thicks.append(layer.d)
    nks.append(layer.nk)
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

