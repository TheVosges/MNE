import ReadDataAndCalcAVRWeveletPower as intro2
import numpy as np
from matplotlib import cm
import sys, os

#Przypisanie odpowiednich wierszów z pliku do odpowiednich grup oraz wykluczenia wierszów z błędem
controlsGroup = [1,24]
controlsError = [11]

depressionGroup = [24,57]
depressionError = [50]

remGroup = [57, 74]
remError = []

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')


# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

"""
    Funkcja mająca na celu zapisanie do folderów uśrednionej wartości odprowadzeń do plików w folderze "/Data" oraz tabelę
    wartości odprowadzeń dla wszystkich osob tej grupy pod "/Data/Raw"
    
    :arg
        group - tablica dwóch wartości - pierwszego oraz ostatniego wersa
        eye-type - rodzaj badania (CE1)
        errorGroup - tablica wierszów do ominięcia
"""
def saveMean(group, eye_type, fa = 10, fc = 1.8, errorGroup = []):
    if group[0] == controlsGroup[0]:
        nameOfGroup = "Controls"
    elif group[0] == depressionGroup[0]:
        nameOfGroup = "Depression"
    else:
        nameOfGroup = "Remission"

    print(nameOfGroup + " - " + eye_type + "_fc" + str(fc) + "_fa" + str(fa))
    blockPrint()

    infoLoc = "bazaEEG.xls"
    CE1Array = []
    for controls in range(group[0], group[1]):
        if controls in errorGroup:
            continue

        eegInfo = intro2.getEEGInfo(infoLoc, controls, eye_type)
        eeg = intro2.readEEGSegment(eegInfo)
        enablePrint()
        print(eegInfo[3])
        blockPrint()
        CE1 = intro2.avrWaveletPower(eeg, fa, fc, False, False, cm.jet, [])
        CE1Array.append(CE1)

    enablePrint()
    CE1Array = np.array(CE1Array)
    CE1Mean = np.mean(CE1Array, axis=0)

    print(CE1Array.shape)
    print(CE1Mean.shape)

    np.save("Data/" + nameOfGroup + "_" + eye_type + "_fc" + str(fc) + "_fa" + str(fa), CE1Mean)
    np.save("Data/Raw/" + nameOfGroup + "_" + eye_type + "_fc" + str(fc) + "_fa" + str(fa), CE1Array)


if __name__ == "__main__":

    fa = [6, 8, 10, 12]
    fc = [1.0, 1.8]

    for fa_single in fa:
        for fc_single in fc:
            saveMean(controlsGroup, "CE1", fa_single, fc_single, controlsError)
            saveMean(depressionGroup, "CE1", fa_single, fc_single, depressionError)
            saveMean(remGroup, "CE1", fa_single, fc_single, remError)

            saveMean(controlsGroup, "OE1", fa_single, fc_single, controlsError)
            saveMean(depressionGroup, "OE1", fa_single, fc_single, depressionError)
            saveMean(remGroup, "OE1", fa_single, fc_single, remError)

            saveMean(controlsGroup, "CE2", fa_single, fc_single, controlsError)
            saveMean(depressionGroup, "CE2", fa_single, fc_single, depressionError)
            saveMean(remGroup, "CE2", fa_single, fc_single, remError)

            saveMean(controlsGroup, "OE2", fa_single, fc_single, controlsError)
            saveMean(depressionGroup, "OE2", fa_single, fc_single, depressionError)
            saveMean(remGroup, "OE2", fa_single, fc_single, remError)

