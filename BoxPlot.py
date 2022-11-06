import numpy as np
import matplotlib.pyplot as plt
import os
#            0      1     2     3    4      5     6      7      8    9    10    11    12    13    14    15    16     17    18    19   20
sensors = ["Fp2", "F8", "T4", "T6", "O2", "Fp1", "F7", "T3", "T5", "O1", "F4", "C4", "P4", "F3", "C3", "P3", "Fpz", "Fz", "Cz", "Pz", "Oz"]
includeEEG = [6, 7, 8, 1, 2, 3, 9, 4, 20]
included = []
for sensor in includeEEG:
    included.append(sensors[sensor])

def filterDataDiff(npArray1, npArray2):
    print(npArray1.shape)
    data = []

    #Stworzenie miejsca na dane dla każdego sensora
    for name in sensors:
        data.append([])

    #Dodanie wartości z pierwszej tabeli do tabeli posortowanych sensorów
    for person in npArray1:
        i = 0
        for sensor in person:
            data[i].append(sensor)
            i+=1

    pomiar_osoby = 0
    for person in npArray2:
        odprowadzenie = 0
        for sensor in person:
            data[odprowadzenie][pomiar_osoby] = data[odprowadzenie][pomiar_osoby] - sensor
            odprowadzenie+=1
        pomiar_osoby += 1

    return data

def sortData(directory, fa, fc):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith("_fc" + str(fc) + "_fa" + str(fa) + ".npy"):
            filePath = os.path.join(directory, filename)
            files.append(filePath)
        else:
            continue
    files.sort()
    print(files)
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


def drawPlots(dataSet):
    fig, axs = plt.subplots(3, 2)


    axs[0, 0].boxplot(dataSet[0], showmeans=True)
    axs[0, 0].set_title('Controls CE1 - OE1')
    axs[0, 0].set_xticklabels(sensors)
    axs[0, 0].set_ylim(-1 * 1e-11, 3 * 1e-11)

    axs[0, 1].boxplot(dataSet[1], showmeans=True)
    axs[0, 1].set_title('Controls CE2 - OE2')
    axs[0, 1].set_xticklabels(sensors)
    axs[0, 1].set_ylim(-1 * 1e-11, 3 * 1e-11)

    axs[1, 0].boxplot(dataSet[2], showmeans=True)
    axs[1, 0].set_title('Depression CE1 - OE1')
    axs[1, 0].set_xticklabels(sensors)
    axs[1, 0].set_ylim(-1 * 1e-11, 3 * 1e-11)

    axs[1, 1].boxplot(dataSet[3], showmeans=True)
    axs[1, 1].set_title('Depression CE2 - OE2')
    axs[1, 1].set_xticklabels(sensors)
    axs[1, 1].set_ylim(-1 * 1e-11, 3 * 1e-11)

    axs[2, 0].boxplot(dataSet[4], showmeans=True)
    axs[2, 0].set_title('Remission CE1 - OE1')
    axs[2, 0].set_xticklabels(sensors)
    axs[2, 0].set_ylim(-1 * 1e-11, 3 * 1e-11)

    axs[2, 1].boxplot(dataSet[5], showmeans=True)
    axs[2, 1].set_title('Remission CE2 - OE2')
    axs[2, 1].set_xticklabels(sensors)
    axs[2, 1].set_ylim(-1 * 1e-11, 3 * 1e-11)

    plt.show()


if __name__ == "__main__":
    filesSorted = sortData("Data/Raw/", 10, 1.8)
    dataSet = []
    for fileNames in filesSorted:
        print(fileNames)
        dataSet.append(filterDataDiff(np.load(fileNames[0]), np.load(fileNames[1])))

    drawPlots(dataSet)
