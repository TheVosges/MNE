import numpy as np
import os
import  scipy

#            0      1     2     3    4      5     6      7      8    9    10    11    12    13    14    15    16     17    18    19   20
sensors = ["Fp2", "F8", "T4", "T6", "O2", "Fp1", "F7", "T3", "T5", "O1", "F4", "C4", "P4", "F3", "C3", "P3", "Fpz", "Fz", "Cz", "Pz", "Oz"]
includeEEG = [6, 7, 8, 1, 2, 3, 9, 4, 20]
includeEEG.sort()
included = []
for sensor in includeEEG:
    included.append(sensors[sensor])

def sortData(directory):
    files = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".npy"):
            filePath = os.path.join(os.getcwd() , filename)
            files.append(filePath)
        else:
            continue
    files.sort()
    return files

def testWithUman(data):
    Controls_CE1 = data[0]
    Controls_OE1 = data[1]
    Controls_CE2 = data[2]
    Controls_OE2 = data[3]
    Depression_CE1 = data[4]
    Depression_OE1 = data[5]
    Depression_CE2 = data[6]
    Depression_OE2 = data[7]
    Remission_CE1 = data[8]
    Remission_OE1 = data[9]
    Remission_CE2 = data[10]
    Remission_OE2 = data[11]

    test_data = {}
    multiple_sensor_data = []
    for i in range(0, len(included)):
        # print(included[i])
        sensor_test_result = []


        result = scipy.stats.mannwhitneyu(Controls_CE1[i], Depression_CE1[i])
        single_result = {"CE1_C_D" : result}
        sensor_test_result.append(single_result)
        result = scipy.stats.mannwhitneyu(Depression_CE1[i], Remission_CE1[i])
        single_result = {"CE1_D_R" : result}
        sensor_test_result.append(single_result)

        result = scipy.stats.mannwhitneyu(Controls_CE2[i], Depression_CE2[i])
        single_result = {"CE2_C_D" : result}
        sensor_test_result.append(single_result)
        result = scipy.stats.mannwhitneyu(Depression_CE2[i], Remission_CE2[i])
        single_result = {"CE2_D_R" : result}
        sensor_test_result.append(single_result)

        result = scipy.stats.mannwhitneyu(Controls_OE1[i], Depression_OE1[i])
        single_result = {"OE1_C_D" : result}
        sensor_test_result.append(single_result)
        result = scipy.stats.mannwhitneyu(Depression_OE1[i], Remission_OE1[i])
        single_result = {"CE2_D_R" : result}
        sensor_test_result.append(single_result)

        result = scipy.stats.mannwhitneyu(Controls_OE2[i], Depression_OE2[i])
        single_result = {"OE2_C_D" : result}
        sensor_test_result.append(single_result)
        result = scipy.stats.mannwhitneyu(Depression_OE2[i], Remission_OE2[i])
        single_result = {"OE2_D_R" : result}
        sensor_test_result.append(single_result)

        sensorDict = {included[i] : sensor_test_result}
        multiple_sensor_data.append(sensorDict)
    test_data[file] = multiple_sensor_data

    return multiple_sensor_data




if __name__ == "__main__":
    files = sortData("/")
    test_data = {}
    for file in files:
        # print(file)
        data = np.load(file, allow_pickle = True)
        file_test_data = testWithUman(data)
        test_data[file] = file_test_data

    for file in test_data.values():
        value = {i for i in test_data if test_data[i] == file}

        for test in file:

            for single_sensor_test in list(test.values())[0]:
                if list(single_sensor_test.values())[0].pvalue < 0.1:
                    print("For file {} and sensor {} the Uman Test p value was {} between {}".format(list(value)[0], list(test.keys())[0], list(single_sensor_test.values())[0].pvalue, list(single_sensor_test.keys())[0]))
                    # print(list(value)[0])
                    # print(list(test.keys())[0])
                    # print(single_sensor_test)

