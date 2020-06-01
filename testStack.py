import numpy as np
import tmm
#import tmm_vw as tmm
import matplotlib.pyplot as plt
from wpv import Layer,Stack

#import pandas as pd

# This whole thing uses microns for length

degree = np.pi/180
#inc_angle = 10.*degree
inc_angle = 0.*degree
        
num_lams = 500
lams = np.linspace(0.3,2.5,num=num_lams)

Glass = Layer(4000,'Rubin-clear_dumb','i',onecol=True)
TiO2 = Layer(0.05,'Siefke','c',onecol=True)
AZO = Layer(0.2,'Treharne','c',onecol=True)
MAPI = Layer(0.5,'Phillips','c')
ITO = Layer(0.2,'Moerland','c',onecol=True)
ZnO = Layer(0.05,'Stelling','c',onecol=True)
PVP = Layer(1500,'Konig','i',onecol=True)


layers = [Glass,ITO,TiO2,MAPI,ZnO,AZO,PVP,Glass]

stack = Stack(layers)

Glass.plotnk(lams)


"""


#layers = [MAPI]

'''
Ttests = []
for lam in lams:
    Ttests.append(np.exp(-4*np.pi*MAPI.k(lam)/lam*MAPI.d))

plt.figure()
plt.plot(lams,Ttests)
plt.show()
'''

layers = [Glass,ITO,TiO2,MAPI,ZnO,ITO,PVP,Glass]
#layers = [Glass,ITO,ITO,MAPI]
#layers = [ITO,TiO2,MAPI,ZnO,ITO,PVP,Glass]
#layers = [Glass,ITO,TiO2,MAPI,ZnO,ITO]
#layers = [MAPI]
#layers = [ITO,ITO,ITO,ITO]
#layers = [Glass,Glass,Glass,Glass]
#layers = [ITO,ITO,TiO2,MAPI,ZnO,ITO,PVP]
#layers = [Glass]


thicks = [tmm.inf]
iorcs = ['i']
for layer in layers:
    thicks.append(layer.d)
    iorcs.append(layer.i_or_c)
thicks.append(tmm.inf)
iorcs.append('i')

thicks_bw = thicks[::-1]
iorcs_bw = iorcs[::-1]

Ts = []
Rfs = []
Rbs = []
EQEs = []

layerchoice = 4

for lam in lams:

    nks = [1]
    for layer in layers:
        nks.append(layer.nk(lam))
    nks.append(1)

    nks_bw = nks[::-1]
    
    front_spol = tmm.inc_tmm('s',nks,thicks,iorcs,inc_angle,lam)
    front_ppol = tmm.inc_tmm('p',nks,thicks,iorcs,inc_angle,lam)
    back_spol = tmm.inc_tmm('s',nks_bw,thicks_bw,iorcs_bw,inc_angle,lam)
    back_ppol = tmm.inc_tmm('p',nks_bw,thicks_bw,iorcs_bw,inc_angle,lam)
    
    EQE_spol = tmm.inc_absorp_in_each_layer(front_spol)[layerchoice]
    EQE_ppol = tmm.inc_absorp_in_each_layer(front_ppol)[layerchoice]
    
    EQEs.append( (EQE_spol + EQE_ppol) / 2. )
    
    Rfs.append( (front_spol['R']+front_ppol['R']) / 2.)
    Rbs.append( (back_spol['R']+back_ppol['R']) / 2.)
    Ts.append( (front_spol['T']+front_ppol['T']) / 2. )


Ts = np.array(Ts)
Rfs = np.array(Rfs)
Rbs = np.array(Rbs)
As = 1-Ts-Rfs
sanities = Ts+Rfs+As

EQEs = np.array(EQEs)

X = np.transpose([lams,EQEs])
np.savetxt('./Output/EQE.txt',X,delimiter=',',header="wavelength [micron], EQE [1]")

Y = np.transpose([lams,Ts,Rfs,Rbs])
np.savetxt('./Output/TRfRb.txt',Y,delimiter=',',header="wavelength [micron], T [1], R_f [1], R_b [1]")

plt.figure()
plt.plot(lams,Rfs,color='magenta',marker=None,label="$R_f$")
plt.plot(lams,Ts,color='green',marker=None,label="$T$")
plt.plot(lams,Rbs,color='purple',marker=None,label="R_b")
plt.plot(lams,As,color='black',marker=None,label="A")
plt.plot(lams,EQEs,color='black',linestyle='--',marker=None,label="EQE")
plt.plot(lams,sanities,color='gold',marker=None,label="sanity check (R+A+T)")
plt.xlabel('wavelength, $\mu$m')
plt.legend()
plt.show()


"""