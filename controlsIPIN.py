# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 16:32:46 2021

@author: Mirek
"""

import xlrd
import pandas as pd


#infoLoc="/Users/mirek/Dropbox/PraceDoktorskie/Pawel/IPINControls/Control1.xlsx"
infoLoc="/Users/mirek/Dropbox/PraceDoktorskie/Pawel/IPINDepression/Depression1.xlsx"
wb=xlrd.open_workbook(infoLoc)
sheet=wb.sheet_by_index(0)
print(sheet.row_values(0))

# for i in range (sheet.nrows) :
#     print (sheet.cell_value(i,0))
    
subject=1   
print (sheet.cell_value(subject,0))    

print ( 'RecordStart:'+ sheet.cell_value(subject,9))   
print ('OE1 Start:'+ sheet.cell_value(subject,11)) 
print ('OE1 Stop:'+ sheet.cell_value(subject,12)) 

test=sheet.cell_value(subject,11)
#dt.time(sheet.cell_value(subject,11))

#t1=pd.Timestamp( sheet.cell_value(subject,11))

#t1=dt.strptime("12:01:01.05", "%H:%M:%S.%f") 

t1=sheet.cell_value(subject,11).split('.')[0].strip()
t2=sheet.cell_value(subject,12).split('.')[0].strip()


#%%
from datetime import datetime
format_string = "%H:%M:%S"
d1 = datetime. strptime(t1, format_string)
d2 = datetime. strptime(t2, format_string)
print( (d2-d1).total_seconds())
#%%

tSplit=sheet.cell_value(subject,11).strip().split('.')
tString=tSplit[0] +'.'+str( int(tSplit[1]*10))

#%%

from datetime import datetime
import xlrd
import mne
import pandas as pd

def getEEGInfo(infoLoc,subject, condition):
    
    if condition=='OE1':
        colStart=10
        colStop=11
        
    elif condition=='CE1':
        print("CE1")
        colStart=12
        colStop=13
        
    elif condition=='OE2':
        colStart=14
        colStop=15
    elif condition=='CE2':
        colStart=16
        colStop=17
    else:
        print('Error')
              

    wb=xlrd.open_workbook(infoLoc)
    sheet=wb.sheet_by_index(0)
    
    format_string = "%H:%M:%S"
    
    recStart=sheet.cell_value(subject,8).split('.')[0].strip()
    t1=sheet.cell_value(subject,colStart).split('.')[0].strip()
    t2=sheet.cell_value(subject,colStop).split('.')[0].strip()
    
    
    dRec = datetime. strptime(recStart, format_string)
    d1 = datetime. strptime(t1, format_string)
    d2 = datetime. strptime(t2, format_string)
    
    segStart=(d1-dRec).total_seconds()
    segStop=(d2-dRec).total_seconds()
    
 
    filePath=sheet.cell_value(subject,6)+sheet.cell_value(subject,7)
    
    return filePath, segStart, segStop

#%%
eegInfo=getEEGInfo(infoLoc,1,'CE1')
print(eegInfo)


#%%

def readEEGSegment(segmentDetails):
    filePath=segmentDetails[0]
    tmin=segmentDetails[1]
    tmax=segmentDetails[2]
    
    print(segmentDetails)
  
    
    raw = mne.io.read_raw_edf(filePath, preload=True)
    raw.crop(tmin=tmin, tmax=tmax)
    eeg=raw.copy()
    eeg.drop_channels( ['EKG','Photic'])
    ch_names=eeg.info['ch_names']
    
    ch_namesSimple=[]
    for s in ch_names:
        print(s)
        res=s.split('-')
        ch=res[0]
        if ch=='FZ': ch='Fz'
        if ch=='PZ': ch='Pz'
        if ch=='CZ': ch='Cz'
        
        ch_namesSimple.append(ch)
        
    montage = mne.channels.make_standard_montage('standard_1020')
    info = mne.create_info( ch_names=ch_namesSimple, sfreq=eeg.info['sfreq'], ch_types='eeg')
    info.set_montage(montage)
    eeg.info=info
    
    eeg.set_montage('standard_1020')
    mne.set_eeg_reference(eeg, ref_channels='average')
    eeg.plot();
    
    
    #data=eeg.get_data()
    #eegCut=data[:,250]
    #mne.viz.plot_topomap(eegCut, eeg.info, vmin=None, vmax=None, cmap='Pastel1')

    return eeg
   
#%%
infoLoc="/Users/mirek/Dropbox/PraceDoktorskie/Pawel/IPINControls/Control1.xlsx"
eegInfo=getEEGInfo(infoLoc,1,'OE1')
eeg=readEEGSegment(eegInfo)



#%%
## This function implements Addison's version of complex Morlet
import numpy.matlib
import numpy as np
def cmorletCWT(signal=None, avec=None, dt=None, f0=None, norm=None):
 
    N = len(signal)
    Nas = len(avec)
    ## FFT of signal

    dfF = 1 / (N*dt)
    fftx = np.fft.fft(signal)

    ff = np.arange(-len(fftx)/2, len(fftx)/2) * dfF

    waveletMatrix = np.zeros((Nas, np.size(ff)))
    fcon = (np.pi ** 0.25)*(2 ** 0.5)

    ## FFT of wavelet
    for i in range(Nas):
        if (norm == 'L2'):
            fftWavelet = np.sqrt(avec[i]) * fcon * np.exp(- 0.5*((2 * np.pi)*((avec[i]) * ff - f0)) ** 2)
        else:
            fftWavelet = fcon * np.exp(-0.5 * (((2*np.pi)*((avec[i]) * ff - f0))) ** 2)

        waveletMatrix[i] = np.fft.ifftshift(fftWavelet)

    fftSigMatrix = np.matlib.repmat(fftx, Nas, 1)
 
    combinedMatrix = np.multiply(fftSigMatrix, waveletMatrix)
    cwtm = np.fft.ifft(combinedMatrix, None, 1)
    return cwtm

#%%
## Addison's wavelet
## Compare numerical calculations with the analytical result: 0.0532752
## Check is OK  
 
import matplotlib.pyplot as plt   
import math

n=2048;
f=30;
fp = 250;
t = np.arange(0,n/fp,1./fp)
x=np.sin(2*math.pi*f*t)
plt.plot(t,x)
plt.show()

fa=30.0;
fc=1.8;
a=(fc)/ fa
coeff= cmorletCWT(x, [a],1./fp, fc, 'L2')
cwtPower=abs(coeff)**2
plt.plot(t,np.transpose(cwtPower)/1)
plt.show()

#%%
def avrWaveletPower(eeg,fa,fc,plotFigure,normByVar,myMap,range):
        sampFreq=eeg.info['sfreq']
        data=eeg.get_data()
        ch_names=eeg.info['ch_names']
        
        a=(fc)/ fa
        
        cwtList=[]
        for row in data:
            coeff= cmorletCWT(row, [a],1./sampFreq, fc, 'L2')
            if (normByVar):
                absCwt2=np.abs(coeff[0])**2 / np.var(data)
            else:
                absCwt2=np.abs(coeff[0])**2
            avrCwt2=np.mean(absCwt2)
            cwtList.append(avrCwt2)
        
        if (plotFigure):
            if len(range) != 2: 
                mne.viz.plot_topomap(cwtList, eeg.info, vmin=None, vmax=None, 
                                     names= ch_names,show_names=True,cmap=myMap)
            else:
                mne.viz.plot_topomap(cwtList, eeg.info, vmin=range[0],
                                     vmax=range[1], names= ch_names,show_names=True,cmap=myMap)
        return  cwtList
 #%%

eegInfo=getEEGInfo(infoLoc,18,'CE1')
eeg=readEEGSegment(eegInfo)

from matplotlib import cm
test=avrWaveletPower(eeg,10,1.8,True,True,cm.jet,[])

#%%
from matplotlib import cm
import numpy as np


infoLoc="/Users/mirek/Dropbox/PraceDoktorskie/Pawel/IPINControls/Control1.xlsx"
#infoLoc="/Users/mirek/Dropbox/PraceDoktorskie/Pawel/IPINDepression/Depression1.xlsx"
#infoLoc="/Users/mirek/Dropbox/PraceDoktorskie/Pawel/IPINRemission/Remission1.xlsx"


freq=10
normByVar=True

resOE = []
for i in range(1,24):
    eegInfo=getEEGInfo(infoLoc,i,'OE1')
    eeg=readEEGSegment(eegInfo)
    avrWav=avrWaveletPower(eeg,freq,1.8,False,normByVar,cm.jet,[])
    resOE.append(avrWav)
    
avrOE=np.array(resOE).mean(0)
ch_names=eeg.info['ch_names']
mne.viz.plot_topomap(avrOE,eeg.info, vmin=None, vmax=None,names= ch_names,show_names=True,cmap=cm.jet)


resCE = []
for i in range(1,24):
    eegInfo=getEEGInfo(infoLoc,i,'CE1')
    eeg=readEEGSegment(eegInfo)
    avrWav=avrWaveletPower(eeg,freq,1.8,False,normByVar,cm.jet,[])
    resCE.append(avrWav)
    
avrCE=np.array(resCE).mean(0)
ch_names=eeg.info['ch_names']
mne.viz.plot_topomap(avrCE,eeg.info, vmin=None, vmax=None,names= ch_names,show_names=True,cmap=cm.jet)

#%%

reactivity=np.divide(np.array(resCE),np.array(resOE)).mean(0)
print(reactivity.mean())
mne.viz.plot_topomap(reactivity,eeg.info, vmin=0, vmax=15,names= ch_names,show_names=True,cmap=cm.jet)

#%%
avrReactivityForSubjects=np.divide(np.array(resCE),np.array(resOE)).mean(1)
print(avrReactivityForSubjects)
print(avrReactivityForSubjects.mean())












