import ReadDataAndCalcAVRWeveletPower
import numpy as np
from matplotlib import cm
import sys, os
from scipy.stats import variation
from BoxPlot import sortData

# Przypisanie odpowiednich wierszów z pliku do odpowiednich grup oraz wykluczenia wierszów z błędem
controlsGroup = [1,24]

depressionGroup = [24, 57]

remGroup = [57, 74]


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


def saveVariationData(filename):

    blockPrint()

    data = np.load("Data/Raw/" + filename)
    variationData = variation(data, axis=0)

    enablePrint()

    print(filename)
    np.save("Data/Variation/"  + "coefficient_of_variation" + filename, variationData)


if __name__ == "__main__":
    for filename in os.listdir("Data/Raw"):
        f = os.path.join("Data/Raw", filename)
        if os.path.isfile(f):
            saveVariationData(filename)
