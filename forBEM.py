import numpy as np
import tmm
import matplotlib.pyplot as plt
from wpv import Layer

#import pandas as pd

# This whole thing uses microns for length

degree = np.pi/180
#inc_angle = 10.*degree
inc_angle = 0.*degree
        
num_lams = 500
lams = np.linspace(0.3,2.5,num=num_lams)

Glass = Layer(4000,'Rubin-clear','i')
TiO2 = Layer(0.05,'Siefke','c')
AZO = Layer(0.2,'Treharne','c')
MAPI = Layer(0.5,'Phillips','c')
ITO = Layer(0.2,'Moerland','c')
ZnO = Layer(0.05,'Stelling','c')
PVP = Layer(1500,'Konig','i')

#Glass = Layer(4000,1.+0.0j)
#FTO = Layer(0.2,1.2+0.02j)

#layers = [Glass,ITO,TiO2,MAPI,ZnO,ITO,PVP,Glass]
#layers = [Glass,ITO,ITO,MAPI]
#layers = [ITO,TiO2,MAPI,ZnO,ITO,PVP,Glass]
#layers = [Glass,ITO,TiO2,MAPI,ZnO,ITO]
layers = [MAPI]
#layers = [ITO,ITO,ITO,ITO]
#layers = [Glass,Glass,Glass,Glass]
#layers = [ITO,ITO,TiO2,MAPI,ZnO,ITO,PVP]
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

thicks_bw = thicks[::-1]
nks_bw = nks[::-1]
iorcs_bw = iorcs[::-1]

Ts = []
Rfs = []
Rbs = []
EQEs = []

for lam in lams:
    
    front_spol = tmm.inc_tmm('s',nks,thicks,iorcs,inc_angle,lam)
    front_ppol = tmm.inc_tmm('p',nks,thicks,iorcs,inc_angle,lam)
    back_spol = tmm.inc_tmm('s',nks_bw,thicks_bw,iorcs_bw,inc_angle,lam)
    back_ppol = tmm.inc_tmm('p',nks_bw,thicks_bw,iorcs_bw,inc_angle,lam)
    
    coh_sout = front_spol['coh_tmm_data_list'][0]
    coh_pout = front_ppol['coh_tmm_data_list'][0]
#    EQE_spol = tmm.absorp_in_each_layer(coh_sout)[3]
    EQE_spol = tmm.absorp_in_each_layer(coh_sout)[1]

#    EQE_ppol = tmm.absorp_in_each_layer(coh_pout)[3]
    EQE_ppol = tmm.absorp_in_each_layer(coh_pout)[1]
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



# will need this later:
# def absorp_in_each_layer(coh_tmm_data):
# note: input is output from coh_tmm()

