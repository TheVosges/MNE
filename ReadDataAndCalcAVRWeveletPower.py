# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 16:32:46 2021

@author: Mirek
"""

from datetime import datetime
import xlrd
import mne
from matplotlib import cm
import matplotlib.pyplot as plt
import pandas as pd
from mne import Epochs, pick_types, events_from_annotations
# Funkcja pozwala na wyciągnięcie danych z pojedyńczego wiersza z tabeli
# infoLoc - plik z danymi
# subject - wiersz
# condition - Oczy zamknięte lub otwarte
def getEEGInfo(infoLoc, subject, condition):

    if condition == 'OE1':
        colStart = 11
        colStop = 12

    elif condition == 'CE1':
        print("CE1")
        colStart = 13
        colStop = 14

    elif condition == 'OE2':
        colStart = 15
        colStop = 16
    elif condition == 'CE2':
        colStart = 17
        colStop = 18
    else:
        print('Error')

    wb = xlrd.open_workbook(infoLoc)
    sheet = wb.sheet_by_index(0)

    format_string = "%H:%M:%S"

    recStart = sheet.cell_value(subject, 9).split('.')[0].strip()
    t1 = sheet.cell_value(subject, colStart).split('.')[0].strip()
    t2 = sheet.cell_value(subject, colStop).split('.')[0].strip()
    type = sheet.cell_value(subject, 1)
    name = sheet.cell_value(subject, 2)
    name = name + "_" + type

    dRec = datetime.strptime(recStart, format_string)
    d1 = datetime.strptime(t1, format_string)
    d2 = datetime.strptime(t2, format_string)

    segStart = (d1 - dRec).total_seconds()
    segStop = (d2 - dRec).total_seconds()

    print('RecordStart:' + sheet.cell_value(subject, 9))
    print(condition + ' Start:' + sheet.cell_value(subject, colStart))
    print(condition + ' Stop:' + sheet.cell_value(subject, colStop))

    filePath = sheet.cell_value(subject, 7) + '/' + sheet.cell_value(subject, 8)

    return filePath, segStart, segStop, name

#Funkcja ta służy do odczytu danych za pomocą MNE, pierwotnie do jej wyświetlenia (zakomentowana linia 84)
def readEEGSegment(segmentDetails):
    filePath = segmentDetails[0]
    tmin = segmentDetails[1]
    tmax = segmentDetails[2]

    print(segmentDetails)

    raw = mne.io.read_raw_edf(filePath, preload=True)
    raw.crop(tmin=tmin, tmax=tmax)
    eeg = raw.copy()
    eeg.drop_channels(['EKG', 'Photic'])
    ch_names = eeg.info['ch_names']

    ch_namesSimple = []
    for s in ch_names:
        print(s)
        res = s.split('-')
        ch = res[0]
        if ch == 'FZ': ch = 'Fz'
        if ch == 'PZ': ch = 'Pz'
        if ch == 'CZ': ch = 'Cz'

        ch_namesSimple.append(ch)

    montage = mne.channels.make_standard_montage('standard_1020')
    info = mne.create_info(ch_names=ch_namesSimple, sfreq=eeg.info['sfreq'], ch_types='eeg')
    info.set_montage(montage)
    eeg.info = info

    eeg.set_montage('standard_1020')
    mne.set_eeg_reference(eeg, ref_channels='average')
    eeg.plot(title = "EDF info")


    return eeg


## This function implements Addison's version of complex Morlet
import numpy.matlib
import numpy as np

#Funkcja generujaca falkę Morleta
def cmorletCWT(signal=None, avec=None, dt=None, f0=None, norm=None):
    N = len(signal)
    Nas = len(avec)
    ## FFT of signal

    dfF = 1 / (N * dt)
    fftx = np.fft.fft(signal)

    ff = np.arange(-len(fftx) / 2, len(fftx) / 2) * dfF

    waveletMatrix = np.zeros((Nas, np.size(ff)))
    fcon = (np.pi ** 0.25) * (2 ** 0.5)

    ## FFT of wavelet
    for i in range(Nas):
        if (norm == 'L2'):
            fftWavelet = np.sqrt(avec[i]) * fcon * np.exp(- 0.5 * ((2 * np.pi) * ((avec[i]) * ff - f0)) ** 2)
        else:
            fftWavelet = fcon * np.exp(-0.5 * (((2 * np.pi) * ((avec[i]) * ff - f0))) ** 2)

        waveletMatrix[i] = np.fft.ifftshift(fftWavelet)

    fftSigMatrix = np.matlib.repmat(fftx, Nas, 1)

    combinedMatrix = np.multiply(fftSigMatrix, waveletMatrix)
    cwtm = np.fft.ifft(combinedMatrix, None, 1)
    return cwtm

#Funkcja porównująca sygnał ze zdefinowaną funkcją falkową
def avrWaveletPower(eeg, fa, fc, plotFigure, normByVar, myMap, range):
    sampFreq = eeg.info['sfreq']
    data = eeg.get_data()
    ch_names = eeg.info['ch_names']

    a = (fc) / fa

    cwtList = []
    for row in data:
        coeff = cmorletCWT(row, [a], 1. / sampFreq, fc, 'L2')
        if (normByVar):
            absCwt2 = np.abs(coeff[0]) ** 2 / np.var(data)
        else:
            absCwt2 = np.abs(coeff[0]) ** 2
        avrCwt2 = np.mean(absCwt2)
        cwtList.append(avrCwt2)

    fig, (ax1) = plt.subplots(ncols=1)
    if (plotFigure):
        print(eeg.info)
        if len(range) != 2:
            im, cm = mne.viz.plot_topomap(cwtList, eeg.info, vmin=None, vmax=None, axes=ax1, show=False,
                                 names=ch_names, show_names=True, cmap=myMap)
        else:
            im, cm = mne.viz.plot_topomap(cwtList, eeg.info, vmin=range[0], axes=ax1, show=False,
                                 vmax=range[1], names=ch_names, show_names=True, cmap=myMap)

    ax_x_start = 0.85
    ax_x_width = 0.04
    ax_y_start = 0.2
    ax_y_height = 0.5
    cbar_ax = fig.add_axes([ax_x_start, ax_y_start, ax_x_width, ax_y_height])
    clb = fig.colorbar(im, cax=cbar_ax)
    clb.ax.set_title("Napięcie [μV]", fontsize=10)
    plt.show()
    return cwtList


#Testowanie działania
if __name__ == "__main__":
    infoLoc="bazaEEG.xls"
    eegInfo = getEEGInfo(infoLoc, 2, 'CE1')
    print("EEG info: " + str(eegInfo))
    eeg = readEEGSegment(eegInfo)

    test = avrWaveletPower(eeg, 10, 1.8, True, False, cm.jet, [])

