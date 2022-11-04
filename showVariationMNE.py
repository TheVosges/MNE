from matplotlib import pyplot as plt
import numpy as np
import mne
import os, sys
import ReadDataAndCalcAVRWeveletPower as intro
from matplotlib import cm

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')


# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

blockPrint()
infoLoc = "bazaEEG.xls"
eegInfo = intro.getEEGInfo(infoLoc, 2, 'CE1')
eeg = intro.readEEGSegment(eegInfo)
enablePrint()
ch_names = ['Fp2', 'F8', 'T4', 'T6', 'O2', 'Fp1', 'F7', 'T3', 'T5', 'O1', 'F4', 'C4', 'P4', 'F3', 'C3', 'P3', 'Fpz', 'Fz', 'Cz', 'Pz', 'Oz']
lib = "Data/Variation"
minVal = float('inf')
maxVal = float('-inf')

def resetMinMax():
    global minVal
    global maxVal
    minVal = float('inf')
    maxVal = float('-inf')

def sortData(directory, fa, fc):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".npy"):
            if fa in filename and fc in filename:
                filePath = os.path.join(directory, filename)
                files.append(filePath)
        else:
            continue
    files.sort()
    filesSorted = []
    i = 0
    temp = []
    temp2 = []
    for file in files:
        if i == 0:
            temp.append(file)
        if i == 1:
            temp2.append(file)
        if i == 2:
            temp.append(file)
        if i == 3:
            temp2.append(file)
            i = 0
            filesSorted.append(temp)
            filesSorted.append(temp2)
            temp = []
            temp2 = []
            continue
        i+=1
    return filesSorted

def showDataDiff(firstDataFilename, secondDataFilename, i):
    CEVariation = np.load(firstDataFilename)
    OEVariation = np.load(secondDataFilename)
    diff = []
    index = 0
    for index in range(0,CEVariation.shape[0]):
        calculate = (OEVariation[index] - CEVariation[index])/CEVariation[index] * 100
        # calculate = CEVariation[index]
        diff.append(calculate)

    global minVal
    global maxVal
    if (min(diff) < minVal):
        minVal = min(diff)
    if (max(diff) > maxVal):
        maxVal = max(diff)

    im, c_m = mne.viz.plot_topomap(diff, eeg.info, vlim=(-100, 100),
                         names=ch_names, cmap=cm.jet, ch_type='mag', show=False, axes=ax[i[0], i[1]])
    return im, c_m

if __name__ == "__main__":
    # fa = input("Provide Fa (6, 8, 10, 12):")
    # fc = input("Provide Fc (1.0, 1.8):")
    #
    # if int(fa) in [6, 8, 10, 12]:
    #     if float(fc) in [1.0, 1.8]:
    fa_d = [6, 8, 10, 12]
    fc_d = [1.0, 1.8]
    for fa in fa_d:
        for fc in fc_d:
            fig, ax = plt.subplots(ncols=3, nrows=2, figsize=(16, 10), gridspec_kw=dict(top=0.9),
                                   sharex=True, sharey=True)
            sortedData = sortData("Data/Variation", str(fa), str(fc))

            i = [0, 0]
            im, c_m = showDataDiff(sortedData[0][0], sortedData[0][1], i)
            i[1] += 1
            im, c_m = showDataDiff(sortedData[2][0], sortedData[2][1], i)
            i[1] += 1
            im, c_m = showDataDiff(sortedData[4][0], sortedData[4][1], i)
            i[1] += 1

            i[1] = 0
            i[0] += 1
            im, c_m = showDataDiff(sortedData[1][0], sortedData[1][1], i)
            i[1] += 1
            im, c_m = showDataDiff(sortedData[3][0], sortedData[3][1], i)
            i[1] += 1
            im, c_m = showDataDiff(sortedData[5][0], sortedData[5][1], i)
            i[1] += 1

            ax[0, 0].set_title('Controls')
            ax[0, 1].set_title('Depression')
            ax[0, 2].set_title('Remission')
            ax[1, 0].set_title('Controls')
            ax[1, 1].set_title('Depression')
            ax[1, 2].set_title('Remission')
            # print(str(minVal) + ":" + str(maxVal))
            ax_x_start = 0.92
            ax_x_width = 0.04
            ax_y_start = 0.2
            ax_y_height = 0.6
            cbar_ax = fig.add_axes([ax_x_start, ax_y_start, ax_x_width, ax_y_height])
            clb = fig.colorbar(im, cax=cbar_ax)
            clb.ax.set_title("Skala", fontsize=10)
            fig.suptitle('Względny współczynnik zmienności dla oczu otwartych i zamkniętych (OE-CE)/CE) (fa = {} fc = {})'.format(fa, fc), fontsize=16)
            # plt.show()
            plt.savefig('Plots/Variation_Fa' + str(fa) + '_Fc' + str(fc) + '.png', dpi=100)
    #     else:
    #         print("Wrong Fc provided")
    # else:
    #     print("Wrong Fa provided")