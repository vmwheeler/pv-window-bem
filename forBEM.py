import numpy as np
import tmm
import matplotlib.pyplot as plt
from wpv import Layer

#import pandas as pd

# This whole thing uses microns for length

degree = np.pi/180
inc_angle = 10.*degree      
        
        
num_lams = 500
lams = np.linspace(0.3,2.5,num=num_lams)

Glass = Layer(4000,'Rubin-clear','i')
TiO2 = Layer(0.05,'Siefke','c')
AZO = Layer(0.2,'Treharne','c')
MAPI = Layer(0.01,'Phillips','c')
ITO = Layer(0.2,'Moerland','c')
ZnO = Layer(0.05,'Stelling','c')
PVP = Layer(1500,'Konig','i')

#Glass = Layer(4000,1.+0.0j)
#FTO = Layer(0.2,1.2+0.02j)

layers = [Glass,ITO,TiO2,MAPI,ZnO,AZO,PVP,Glass]
#layers = [Glass]

thicks = [tmm.inf]
nks = [1]
iorcs = ['i']
for layer in layers:
    thicks.append(layer.d)
    nks.append(layer.nk(1.1))
    iorcs.append(layer.i_or_c)
thicks.append(tmm.inf)
nks.append(1)
iorcs.append('i')


Ts = []
Rfs = []
Rbs = []

for lam in lams:
    
    front_spol = tmm.inc_tmm('s',nks,thicks,iorcs,inc_angle,lam)
    front_ppol = tmm.inc_tmm('p',nks,thicks,iorcs,inc_angle,lam)
    #back_spol = tmm.coh_tmm_reverse('s',nks,thicks,inc_angle,lam)
    #back_ppol = tmm.coh_tmm_reverse('p',nks,thicks,inc_angle,lam)
    
    Rfs.append( (front_spol['R']+front_ppol['R']) / 2.)
    #Rbs.append( (back_spol['R']+back_ppol['R']) / 2.)
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

