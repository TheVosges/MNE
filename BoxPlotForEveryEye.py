import numpy as np
import matplotlib.pyplot as plt
import os
#            0      1     2     3    4      5     6      7      8    9    10    11    12    13    14    15    16     17    18    19   20
sensors = ["Fp2", "F8", "T4", "T6", "O2", "Fp1", "F7", "T3", "T5", "O1", "F4", "C4", "P4", "F3", "C3", "P3", "Fpz", "Fz", "Cz", "Pz", "Oz"]
includeEEG = [6, 7, 8, 1, 2, 3, 9, 4, 20]
includeEEG.sort()
included = []
for sensor in includeEEG:
    included.append(sensors[sensor])

def filterDataBySensor(npArray):
    data = []

    #Stworzenie miejsca na dane dla każdego sensora
    for name in sensors:
        data.append([])

    #Dodanie wartości z tabeli do tabeli posortowanych sensorów
    for person in npArray:
        i = 0
        for sensor in person:
            data[i].append(sensor)
            i+=1

    #Sortowanie po chcianych sensorach
    dataIncluded = []
    for odprowadzenie in includeEEG:
        dataIncluded.append(data[odprowadzenie])

    return dataIncluded

def sortData(directory, fa, fc):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith("_fc" + str(fc) + "_fa" + str(fa) + ".npy"):
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


def drawPlots(dataSet, fa, fc, scale = True, scaleFrom = -1 * 1e-12, scaleTo = 9 * 1e-12):
    fig, axs = plt.subplots(6, 2, figsize=(16, 8))
    fig.suptitle(
        'Wykresy pudełkowe wartości odprowadzeń (fa = {} fc = {})'.format(fa, fc),
        fontsize=16)
    fig.tight_layout()

    axs[0, 0].boxplot(dataSet[0], showmeans=True)
    axs[0, 0].set_title('Controls CE1')
    axs[0, 0].set_xticklabels(included)
    if scale:
        axs[0, 0].set_ylim(scaleFrom, scaleTo)

    axs[0, 1].boxplot(dataSet[1], showmeans=True)
    axs[0, 1].set_title('Controls OE1')
    axs[0, 1].set_xticklabels(included)
    if scale:
        axs[0, 1].set_ylim(scaleFrom, scaleTo)

    axs[1, 0].boxplot(dataSet[2], showmeans=True)
    axs[1, 0].set_title('Controls CE2')
    axs[1, 0].set_xticklabels(included)
    if scale:
        axs[1, 0].set_ylim(scaleFrom, scaleTo)

    axs[1, 1].boxplot(dataSet[3], showmeans=True)
    axs[1, 1].set_title('Controls OE2')
    axs[1, 1].set_xticklabels(included)
    if scale:
        axs[1, 1].set_ylim(scaleFrom, scaleTo)

    axs[2, 0].boxplot(dataSet[4], showmeans=True)
    axs[2, 0].set_title('Depression CE1')
    axs[2, 0].set_xticklabels(included)
    if scale:
        axs[2, 0].set_ylim(scaleFrom, scaleTo)

    axs[2, 1].boxplot(dataSet[5], showmeans=True)
    axs[2, 1].set_title('Depression OE1')
    axs[2, 1].set_xticklabels(included)
    if scale:
        axs[2, 1].set_ylim(scaleFrom, scaleTo)



    axs[3, 0].boxplot(dataSet[6], showmeans=True)
    axs[3, 0].set_title('Depression CE2')
    axs[3, 0].set_xticklabels(included)
    if scale:
        axs[3, 0].set_ylim(scaleFrom, scaleTo)

    axs[3, 1].boxplot(dataSet[7], showmeans=True)
    axs[3, 1].set_title('Depression OE2')
    axs[3, 1].set_xticklabels(included)
    if scale:
        axs[3, 1].set_ylim(scaleFrom, scaleTo)

    axs[4, 0].boxplot(dataSet[8], showmeans=True)
    axs[4, 0].set_title('Remission CE1')
    axs[4, 0].set_xticklabels(included)
    if scale:
        axs[4, 0].set_ylim(scaleFrom, scaleTo)

    axs[4, 1].boxplot(dataSet[9], showmeans=True)
    axs[4, 1].set_title('Remission OE1')
    axs[4, 1].set_xticklabels(included)
    if scale:
        axs[4, 1].set_ylim(scaleFrom, scaleTo)

    axs[5, 0].boxplot(dataSet[10], showmeans=True)
    axs[5, 0].set_title('Remission CE2')
    axs[5, 0].set_xticklabels(included)
    if scale:
        axs[5, 0].set_ylim(scaleFrom, scaleTo)

    axs[5, 1].boxplot(dataSet[11], showmeans=True)
    axs[5, 1].set_title('Remission OE2')
    axs[5, 1].set_xticklabels(included)
    if scale:
        axs[5, 1].set_ylim(scaleFrom, scaleTo)

    # plt.show()
    if scale:
        plt.savefig('Plots/BoxPlots/Skalowane/BoxPlot_Fa' + str(fa) + '_Fc' + str(fc) + '_scaled.png', dpi=100)
    else:
        plt.savefig('Plots/BoxPlots/BoxPlot_Fa' + str(fa) + '_Fc' + str(fc) + '.png', dpi=100)

if __name__ == "__main__":
    # fa = input("Provide Fa (6, 8, 10, 12):")
    # fc = input("Provide Fc (1.0, 1.8):")
    fa_d = [6, 8, 10, 12]
    fc_d = [1.0, 1.8]
    for fa in fa_d:
        for fc in fc_d:
            filesSorted = sortData("Data/Raw/", fa, fc)
            dataSet = []
            for fileNames in filesSorted:
                for file in fileNames:
                    print("{}_fa{}_fc{}".format(file,fa,fc))
                    dataSet.append(filterDataBySensor(np.load(file)))

            #DataSet to lista
            #      sensorów dla każdego pliku (CE1 CE2 OE1 OE2) * (Controls Depression Remission)
            #           Każdy posiadający po 23, 32 lub 17 rekordów
            drawPlots(dataSet, fa, fc, scale=True, scaleFrom= -1 * 1e-12, scaleTo= 7 * 1e-12)
