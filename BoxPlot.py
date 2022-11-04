import numpy as np
import matplotlib.pyplot as plt
import os

sensors = ["Fp2", "F8", "T4", "T6", "O2", "Fp1", "F7", "T3", "T5", "O1",
           "F4", "C4", "P4", "F3", "C3", "P3", "Fpz", "Fz", "Cz", "Pz", "Oz"]

def filterDataDiff(npArray1, npArray2):

    data = []
    for name in sensors:
        data.append([])

    for person in npArray1:
        i = 0
        for sensor in person:
            data[i].append(sensor)
            i+=1
    print(data)
    j = 0
    for person in npArray2:
        i = 0
        for sensor in person:
            data[i][j] = data[i][j] - sensor
            # data[i][j] = ((data[i][j] - sensor)/data[i][j])*100
            i+=1
        j += 1

    return data

def sortData(directory):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".npy"):
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
    filesSorted = sortData("Data/Raw/")

    dataSet = []
    for fileNames in filesSorted:
        dataSet.append(filterDataDiff(np.load(fileNames[0]), np.load(fileNames[1])))

    drawPlots(dataSet)
