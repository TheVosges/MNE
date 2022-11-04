import os, numpy as np
if __name__ == "__main__":
    for filename in os.listdir("Data/Variation"):
        f = os.path.join("Data/Variation", filename)
        if os.path.isfile(f):
            print(filename)
            print(np.load("Data/Variation/" + filename))
