import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import xlrd
import mne
from sklearn.pipeline import Pipeline
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import ShuffleSplit, cross_val_score
import re

from mne import Epochs, pick_types, events_from_annotations
from mne.channels import make_standard_montage
from mne.io import concatenate_raws, read_raw_edf
from mne.datasets import eegbci
from mne.decoding import CSP

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
    filePath =  "C:/Users/arkad/Desktop/PRACA DYPLOMOWA/" + segmentDetails[0]
    tmin1 = segmentDetails[1]
    tmax1 = segmentDetails[2]

    print(segmentDetails)

    raw = mne.io.read_raw_edf(filePath, preload=True)
    raw.crop(tmin=tmin1, tmax=tmax1)
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
    picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False,
                       exclude='bads')
    print("TEST")
    print(picks)
    print(raw.info)
    events, _ = events_from_annotations(raw, event_id=dict(T1=2, T2=3))
    # Read epochs (train will be done only between 1 and 2s)
    # Testing will be done with a running classifier
    print(tmin1)
    print(tmax1)
    epochs = Epochs(raw, np.array([[0, 0, 0]]), tmin=tmin1, tmax=tmax1, proj=True, picks=picks,
                    baseline=None, preload=True)
    epochs_train = epochs.copy().crop(tmin=tmin1, tmax=tmin1+1)
    labels = epochs.events[:, -1] - 2

    # Define a monte-carlo cross-validation generator (reduce variance):
    scores = []
    epochs_data = epochs.get_data()

    # Assemble a classifier
    csp = CSP(n_components=4, reg=None, log=True, norm_trace=False)

    # plot CSP patterns estimated on full data for visualization
    # csp.fit_transform(epochs_data, labels)

    fig = csp.plot_patterns(epochs.info, ch_type='eeg', units='Patterns (AU)', size=1.5)
    plt.show()
    # return eeg

if __name__ == "__main__":
    print(__doc__)
    infoLoc= "C:/Users/arkad/Desktop/PRACA DYPLOMOWA/bazaEEG.xls"
    eegInfo = getEEGInfo(infoLoc, 2, 'CE1')
    print("EEG info: " + str(eegInfo))
    raw = readEEGSegment(eegInfo)







