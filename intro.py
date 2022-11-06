# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 16:32:46 2021

@author: Mirek
"""

from datetime import datetime
import xlrd
import mne
import pandas as pd

def getEEGInfo(infoLoc,subject, condition):
    
    if condition=='OE1':
        colStart=11
        colStop=12
        
    elif condition=='CE1':
        print("CE1")
        colStart=13
        colStop=14
        
    elif condition=='OE2':
        colStart=15
        colStop=16
    elif condition=='CE2':
        colStart=17
        colStop=18
    else:
        print('Error')
    

    wb=xlrd.open_workbook(infoLoc)
    sheet=wb.sheet_by_index(0)
    
    format_string = "%H:%M:%S"
    
    recStart=sheet.cell_value(subject,9).split('.')[0].strip()
    t1=sheet.cell_value(subject,colStart).split('.')[0].strip()
    t2=sheet.cell_value(subject,colStop).split('.')[0].strip()
    
    
    dRec = datetime. strptime(recStart, format_string)
    d1 = datetime. strptime(t1, format_string)
    d2 = datetime. strptime(t2, format_string)
    
    segStart=(d1-dRec).total_seconds()
    segStop=(d2-dRec).total_seconds()
    
    
    print ( 'RecordStart:'+ sheet.cell_value(subject,9))   
    print (condition +' Start:'+ sheet.cell_value(subject,colStart)) 
    print (condition +' Stop:'+ sheet.cell_value(subject,colStop))  
    
 
    filePath=sheet.cell_value(subject,7)+'/'+sheet.cell_value(subject,8)
    
    return filePath, segStart, segStop


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
    
    

    return eeg
   
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
if __name__ == "__main__":
    infoLoc="/Users/mirek/Dropbox/RobertK/PMR/bazaEEG.xls"
    eegInfo=getEEGInfo(infoLoc,2,'CE1')
    print(eegInfo)
    eeg=readEEGSegment(eegInfo)

    #%%

    from matplotlib import cm
    test=avrWaveletPower(eeg,10,1.8,True,False,cm.jet,[])

    #%%












