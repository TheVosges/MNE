from matplotlib import pyplot as plt
from showVariationMNE import sortData
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

def showDataDiff(firstDataFilename, secondDataFilename, i):
    CEVariation = np.load(firstDataFilename)
    OEVariation = np.load(secondDataFilename)
    OE1 = []
    CE1 = []
    index = 0
    for index in range(0,CEVariation.shape[0]):
        OE1.append(OEVariation[index])
        CE1.append(CEVariation[index])
    global minVal
    global maxVal
    if (min(CE1) < minVal):
        minVal = min(CE1)
    if (max(CE1) > maxVal):
        maxVal = max(CE1)
    if (min(OE1) < minVal):
        minVal = min(OE1)
    if (max(OE1) > maxVal):
        maxVal = max(OE1)

    im, c_m = mne.viz.plot_topomap(OE1, eeg.info, vlim=(0, 2),
                         names=ch_names, cmap=cm.jet, ch_type='mag', show=False, axes=ax[i[0], i[1]])
    im2, c_m2 = mne.viz.plot_topomap(CE1, eeg.info, vlim=(0, 2),
                         names=ch_names, cmap=cm.jet, ch_type='mag', show=False, axes=ax[i[0], i[1]+3])
    return im, c_m



if __name__ == "__main__":
    # fa = input("Provide Fa (6, 8, 10, 12):")
    # fc = input("Provide Fc (1.0, 1.8):")
    #
    # if int(fa) in [6, 8, 10, 12]:
    #     if float(fc) in [1.0, 1.8]:
    fa_d = [6, 8 ,10 ,12]
    fc_d = [1.0, 1.8]
    for fa in fa_d:
        for fc in fc_d:
            sortedData = sortData("Data/Variation", str(fa), str(fc))
            fig, ax = plt.subplots(ncols=6, nrows=2, figsize=(16, 8), gridspec_kw=dict(top=0.9),
                                   sharex=True, sharey=True)
            i = [0, 0]
            im, c_m = showDataDiff(sortedData[0][0], sortedData[0][1], i)
            i[1] += 1
            im, c_m = showDataDiff(sortedData[2][0], sortedData[2][1], i)
            i[1] += 1
            im, c_m = showDataDiff(sortedData[4][0], sortedData[4][1], i)

            i[1] = 0
            i[0] += 1
            im, c_m = showDataDiff(sortedData[1][0], sortedData[1][1], i)
            i[1] += 1
            im, c_m = showDataDiff(sortedData[3][0], sortedData[3][1], i)
            i[1] += 1
            im, c_m = showDataDiff(sortedData[5][0], sortedData[5][1], i)

            ax[0, 0].set_title('Controls OE1')
            ax[0, 3].set_title('Controls CE1')
            ax[0, 1].set_title('Depression OE1')
            ax[0, 4].set_title('Depression CE1')
            ax[0, 2].set_title('Remission OE1')
            ax[0, 5].set_title('Remission CE1')
            ax[1, 0].set_title('Controls OE2')
            ax[1, 3].set_title('Controls CE2')
            ax[1, 1].set_title('Depression OE2')
            ax[1, 4].set_title('Depression CE2')
            ax[1, 2].set_title('Remission OE2')
            ax[1, 5].set_title('Remission CE2')
            # print(str(minVal) + ":" + str(maxVal))
            ax_x_start = 0.93
            ax_x_width = 0.04
            ax_y_start = 0.2
            ax_y_height = 0.6
            cbar_ax = fig.add_axes([ax_x_start, ax_y_start, ax_x_width, ax_y_height])
            clb = fig.colorbar(im, cax=cbar_ax)
            clb.ax.set_title("Skala", fontsize=10)
            fig.suptitle('Bezwzględny współczynnik zmienności dla oczu otwartych i zamkniętych (fa = {} fc = {})'.format(fa, fc) , fontsize=16)
            # plt.show()
            plt.savefig('Plots/Variation_CEleft_OEright_Sep_Fa' + str(fa) + '_Fc' + str(fc) + '.png', dpi=100)
    #     else:
    #         print("Wrong Fc provided")
    # else:
    #     print("Wrong Fa provided")

