import numpy as np
import mne
from matplotlib import cm
from matplotlib import pyplot as plt
import ReadDataAndCalcAVRWeveletPower as intro
import sys, os

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
minVal = float('inf')
maxVal = float('-inf')

def showDataDiff(firstDataFilename, secondDataFilename, i):
    CEMean = np.load(firstDataFilename)
    OEMean = np.load(secondDataFilename)

    diff = []
    index = 0
    for index in range(0,CEMean.shape[0]):
        diff.append((((OEMean[index] - CEMean[index])/CEMean[index])*100))
    global minVal
    global maxVal
    if (min(diff) < minVal):
        minVal = min(diff)
    if (max(diff) > maxVal):
        maxVal = max(diff)

    im, c_m = mne.viz.plot_topomap(diff, eeg.info, vlim=(-100, 100),
                         names=ch_names, cmap=cm.jet, ch_type='eeg', show=False, axes=ax[i[0], i[1]])

    return im, c_m

if __name__ == "__main__":
    fa = input("Provide Fa (6, 8, 10, 12):")
    fc = input("Provide Fc (1.0, 1.8):")
    if int(fa) in [6, 8, 10, 12]:
        if float(fc) in [1.0, 1.8]:
    # fa_d = [6, 8, 10, 12]
    # fc_d = [1.0, 1.8]
    # for fa in fa_d:
    #     for fc in fc_d:
            fig, ax = plt.subplots(ncols=3, nrows=2, figsize=(16, 10), gridspec_kw=dict(top=0.9),
                                   sharex=True, sharey=True)
            i = [0, 0]
            im, c_m = showDataDiff("Data/Controls_CE1_fc" + str(fc) + "_fa" + str(fa) + ".npy", "Data/Controls_OE1_fc" + str(fc) + "_fa" + str(fa) + ".npy", i)
            i[1] += 1
            im, c_m = showDataDiff("Data/Depression_CE1_fc" + str(fc) + "_fa" + str(fa) + ".npy", "Data/Depression_OE1_fc" + str(fc) + "_fa" + str(fa) + ".npy", i)
            i[1] += 1
            im, c_m = showDataDiff("Data/Remission_CE1_fc" + str(fc) + "_fa" + str(fa) + ".npy", "Data/Remission_OE1_fc" + str(fc) + "_fa" + str(fa) + ".npy", i)
            i[1] += 1

            i[1] = 0
            i[0] += 1
            im, c_m = showDataDiff("Data/Controls_CE2_fc" + str(fc) + "_fa" + str(fa) + ".npy", "Data/Controls_OE2_fc" + str(fc) + "_fa" + str(fa) + ".npy", i)
            i[1] += 1
            im, c_m = showDataDiff("Data/Depression_CE2_fc" + str(fc) + "_fa" + str(fa) + ".npy", "Data/Depression_OE2_fc" + str(fc) + "_fa" + str(fa) + ".npy", i)
            i[1] += 1
            im, c_m = showDataDiff("Data/Remission_CE2_fc" + str(fc) + "_fa" + str(fa) + ".npy", "Data/Remission_OE2_fc" + str(fc) + "_fa" + str(fa) + ".npy", i)
            i[1] += 1

            ax[0, 0].set_title('Controls OE1_CE1')
            ax[0, 1].set_title('Depression OE1_CE1')
            ax[0, 2].set_title('Remission OE1_CE1')
            ax[1, 0].set_title('Controls OE2_CE2')
            ax[1, 1].set_title('Depression OE2_CE2')
            ax[1, 2].set_title('Remission OE2_CE2')
            # print(str(minVal) + ":" + str(maxVal))

            ax_x_start = 0.92
            ax_x_width = 0.04
            ax_y_start = 0.2
            ax_y_height = 0.6
            cbar_ax = fig.add_axes([ax_x_start, ax_y_start, ax_x_width, ax_y_height])
            clb = fig.colorbar(im, cax=cbar_ax)
            clb.ax.set_title("Skala", fontsize=10)
            fig.suptitle('', fontsize=16)
            fig.suptitle('Względna średnia moc falkowa dla oczu otwartych i zamkniętych (OE-CE)/CE (fa = {} fc = {})'.format(fa, fc), fontsize=16)
            # plt.show()
            plt.savefig('Plots/AVG_Fa' + str(fa) + '_Fc' + str(fc) + '.png', dpi = 100)
        else:
            print("Wrong Fc provided")
    else:
        print("Wrong Fa provided")
