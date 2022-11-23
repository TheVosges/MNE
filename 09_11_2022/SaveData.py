import CalculateData as intro2
import numpy as np
from matplotlib import cm, pyplot as plt
import sys, os

#Przypisanie odpowiednich wierszów z pliku do odpowiednich grup oraz wykluczenia wierszów z błędem
dataGroup = [1,4]
dataError = [0]

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
    print(eye_type + "_fc" + str(fc) + "_fa" + str(fa))
    blockPrint()

    infoLoc = "bazaEEG_newData.xls"
    CE1Array = []
    for controls in range(group[0], group[1]+1):
        print(controls)
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

    np.save("Data/" + eye_type + "_fc" + str(fc) + "_fa" + str(fa), CE1Mean)
    np.save("Data/Raw/" + eye_type + "_fc" + str(fc) + "_fa" + str(fa), CE1Array)


if __name__ == "__main__":
    fa = [6, 8]
    fc = [1.0, 1.8]
    for fa_single in fa:
        for fc_single in fc:
            saveMean(dataGroup, "CE1", fa_single, fc_single, dataError)

            saveMean(dataGroup, "OE1", fa_single, fc_single, dataError)

            saveMean(dataGroup, "CE2", fa_single, fc_single, dataError)

            saveMean(dataGroup, "OE2", fa_single, fc_single, dataError)

            saveMean(dataGroup, "CE3", fa_single, fc_single, dataError)

            saveMean(dataGroup, "OE3", fa_single, fc_single, dataError)

            saveMean(dataGroup, "CE4", fa_single, fc_single, dataError)

            saveMean(dataGroup, "OE4", fa_single, fc_single, dataError)

